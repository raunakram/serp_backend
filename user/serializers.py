from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    seo_api_token = serializers.CharField(required=False, allow_blank=True)  


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'seo_api_token')


    def create(self, validated_data):
        validated_data.pop('password2')
        seo_api_token = validated_data.pop('seo_api_token', '')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.seo_api_token = seo_api_token
        user.save()

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
