from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    username = None
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get('request'),
                            email=email, password=password)
            
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.is_active:
            raise serializers.ValidationError("Please activate your account with the activation link.")
        
        attrs['user'] = user
        return super().validate(attrs)
        

