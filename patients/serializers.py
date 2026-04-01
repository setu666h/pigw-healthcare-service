from rest_framework import serializers

class PatientIntakeSerializer(serializers.Serializer):
    resourceType = serializers.CharField()
    id = serializers.CharField()
    name = serializers.ListField()
    gender = serializers.CharField()
    birthDate = serializers.DateField()
    identifier = serializers.ListField(required=False)