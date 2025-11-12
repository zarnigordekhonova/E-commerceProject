from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = (
            "full_name",
            "username",
            "email",
            "password",
        )
        extra_kwargs = {"password" : {"write_only": True}}

    def create(self, validated_data):
        user =  User(
            full_name = validated_data["full_name"],
            username = validated_data["username"],
            email = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user
    
    def to_representation(self, instance):
        return { 
            "Username": instance.username,
            "Email address": instance.email,
        }
        


