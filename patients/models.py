from django.db import models

class PatientRecord(models.Model):
    patient_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField()

    ssn_encrypted = models.BinaryField(null=True, blank=True)
    passport_encrypted = models.BinaryField(null=True, blank=True)

    raw_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_id


class AccessLog(models.Model):
    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.patient.patient_id} accessed at {self.accessed_at}"