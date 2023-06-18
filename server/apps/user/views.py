from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .logic.serializers import (
    RegistrationSerializer,
    ProfileSerializer,
)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email_phone": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, default="Credentials missing"
                    ),
                },
            ),
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, default="Invalid Credentials"
                    ),
                },
            ),
        },
    )
    def post(self, request):
        email_phone = request.data.get("email_phone")
        password = request.data.get("password")

        if email_phone is None or password is None:
            return Response("Credentials missing", status=status.HTTP_400_BAD_REQUEST)

        if "@" in email_phone:
            email = User.objects.filter(email=email_phone).first().email
        else:
            email = User.objects.filter(phone=email_phone).first().email

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            return Response({**user.get_tokens()}, status=status.HTTP_200_OK)

        return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)


class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={
            201: RegistrationSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, default="Invalid Credentials"
                    ),
                    "errors": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "field": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING),
                            ),
                        },
                    ),
                },
            ),
        },
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"message": "Invalid Credentials", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            205: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, default="Logout successful"
                    ),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, default="Invalid token"
                    ),
                },
            ),
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default="Authentication credentials were not provided.",
                    ),
                },
            ),
        },
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: ProfileSerializer,
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default="Authentication credentials were not provided or is incorrect.",
                    ),
                },
            ),
        },
    )
    def get(self, request):
        user = request.user
        return Response(ProfileSerializer(user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={
            200: ProfileSerializer,
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default="Authentication credentials were not provided or is incorrect.",
                    ),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, default="Invalid Data"
                    ),
                    "errors": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "field": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING),
                            ),
                        },
                    ),
                },
            ),
        },
    )
    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid Data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"message": "Email does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )

        otp = user.generate_otp()

        send_mail(
            "Sufle Reset Password",
            f"Your OTP Code is: {otp}",
            settings.EMAIL_HOST_USER,
            [email],
        )

        return Response({"message": "OTP sent."}, status=status.HTTP_200_OK)


class CheckOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response(
                {"message": "Email and OTP is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"message": "Email does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not user.verify_otp(otp):
            return Response(
                {"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "OTP is valid.", **user.get_tokens()}, status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not password or not confirm_password:
            return Response(
                {"message": "Password and Confirm Password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != confirm_password:
            return Response(
                {"message": "Password and Confirm Password does not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save()

        return Response({"message": "Password updated."}, status=status.HTTP_200_OK)
