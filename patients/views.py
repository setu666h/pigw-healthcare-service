from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PatientRecord, AccessLog
from .serializers import PatientIntakeSerializer
from .utils import encrypt_data, decrypt_data, mask_ssn
from .tasks import run_async_email


def is_adult(birth_date):
    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    return age >= 18


class PatientIntakeView(APIView):

    def post(self, request):
        serializer = PatientIntakeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        # Check age
        if not is_adult(data['birthDate']):
            return Response({"error": "Patient must be 18+"}, status=400)

        # Get SSN from identifier
        ssn = None
        identifiers = data.get("identifier", [])
        for item in identifiers:
            if "ssn" in item.get("system", ""):
                ssn = item.get("value")

        encrypted_ssn = encrypt_data(ssn) if ssn else None

        # Get name
        name = data["name"][0]
        full_name = f"{name.get('given', [''])[0]} {name.get('family', '')}"

        # Save to DB
        patient = PatientRecord.objects.create(
            patient_id=data["id"],
            name=full_name,
            gender=data["gender"],
            birth_date=data["birthDate"],
            ssn_encrypted=encrypted_ssn,
            raw_data=request.data
        )
        # email
        run_async_email(full_name)

        return Response({"message": "Patient stored"}, status=201)


class PatientDetailView(APIView):

    def get(self, request, patient_id):
        try:
            patient = PatientRecord.objects.get(patient_id=patient_id)
        except PatientRecord.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)

        # Decrypt SSN
        ssn = None
        if patient.ssn_encrypted:
            ssn = decrypt_data(patient.ssn_encrypted)

        # Mask SSN
        masked_ssn = mask_ssn(ssn) if ssn else None

        # Log access
        ip = self.get_client_ip(request)
        user = request.user.username if request.user.is_authenticated else "anonymous"

        AccessLog.objects.create(
            patient=patient,
            ip_address=ip,
            user=user
        )

        return Response({
            "patient_id": patient.patient_id,
            "name": patient.name,
            "gender": patient.gender,
            "birth_date": patient.birth_date,
            "ssn": masked_ssn
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')