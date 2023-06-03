from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class LoginView(APIView):
    
    def post(self, request):
        email_phone = request.data.get('email_phone')
        password = request.data.get('password')

        if email_phone is None or password is None:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        if '@' in email_phone:
            email = User.objects.filter(email=email_phone).first().email  
        else:
            email = User.objects.filter(phone=email_phone).first().email
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)

            response = {
                'msg': 'Login Success',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(response, status=status.HTTP_200_OK)
        
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)