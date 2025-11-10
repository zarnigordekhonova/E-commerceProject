from rest_framework import serializers

from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserGetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "full_name",
            "username",
            "email",
        )
        read_only_fields = (
            "created_at", 
        )