# tasks/serializers.py
from rest_framework import serializers
from UserResponse.models import UserRegisterModel


class UserRegisterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegisterModel
        fields = [
            "name",
            "surname",
            "email",
            "phone_number",
            "season_type",
            "season_number",
        ]
