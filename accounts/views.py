from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import APIView
from .models import CustomUser, EmailConfirmation
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status    
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class EmailConfirmView(APIView):
    def get(self, request, token):
        try:
            confirm = EmailConfirmation.objects.get(token = token)
            user = confirm.user
            user.is_active = True
            user.is_email_confirmed = True
            user.save()
            confirm.delete()
            return Response({'message':'Email confirmed'})
        except EmailConfirmation.DoesNotExist:
            return Response({"Messagae":'invalid or expired roken'}, status=400)
        
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
