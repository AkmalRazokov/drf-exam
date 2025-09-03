from rest_framework import serializers
from .models import CustomUser, EmailConfirmation
from django.core.mail import send_mail
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        confirm = EmailConfirmation.objects.create(user = user)
        self.send_email_confirmation(user.email, confirm.token)
        return user

    def send_email_confirmation(self, email, token):
        confirm_link = f"http://127.0.0.1:8000/auth/confirm-email/{token}"
        send_mail(
            "Confirm your email",
        
            f"Click here to confirm: {confirm_link}",
        
            "rmaks8048@gmail.com",
        
            [email],
            )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email = email, password = password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_email_confirmed:
            raise serializers.ValidationError('Email not confirmed')
        data['user'] = user
        return data