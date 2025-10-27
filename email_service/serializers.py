
from rest_framework import serializers

class CareerFormSerializer(serializers.Serializer):

    role = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    current_city = serializers.CharField(required=True, allow_blank=True)
    experience_years = serializers.IntegerField(required=True, allow_null=True)
    experience_months = serializers.IntegerField(required=True,  allow_null=True)
    preferred_location = serializers.CharField(required=False, allow_blank=True)
    other_location = serializers.CharField(required=False, allow_blank=True)
    resume = serializers.FileField(required=False, allow_null=True)  # Optional file


class ContactSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, allow_blank=True)
    locationState = serializers.CharField(max_length=100, allow_blank=True)
    message = serializers.CharField()