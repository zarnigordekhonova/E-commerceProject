from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("You must enter your registered email and password.")
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
        )
    
