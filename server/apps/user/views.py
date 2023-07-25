from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from server.apps.core.logic.permissions import IsStaff, IsAdmin
from server.apps.core.logic.schemas import (
    SUCCESS,
    BAD_REQUEST,
    UNAUTHORIZED,
    NO_CONTENT,
)

from .models import User
from .logic.serializers import UserSerializer, LoginSerializer
from .logic.schemas import AUTH_TOKENS


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: AUTH_TOKENS,
            400: BAD_REQUEST,
            401: UNAUTHORIZED,
        },
    )
    def post(self, request):
        """Login view for user."""

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data["email_phone"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "Giriş məlumatları yanlışdır!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)

        return Response({**user.get_tokens()}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: BAD_REQUEST},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            205: NO_CONTENT,
            400: BAD_REQUEST,
            401: UNAUTHORIZED,
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
            200: UserSerializer,
            401: UNAUTHORIZED,
        },
    )
    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: BAD_REQUEST,
            401: UNAUTHORIZED,
        },
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid Data", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: SUCCESS,
            400: BAD_REQUEST,
        },
    )
    def post(self, request):
        try:
            email = request.data["email"]
        except Exception:
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "otp": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: AUTH_TOKENS,
            400: BAD_REQUEST,
        },
    )
    def post(self, request):
        try:
            email = request.data["email"]
            otp = request.data["otp"]
        except Exception:
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "confirm_password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: NO_CONTENT,
            400: BAD_REQUEST,
            401: UNAUTHORIZED,
        },
    )
    def post(self, request):
        user = request.user

        try:
            password = request.data["password"]
            confirm_password = request.data["confirm_password"]
        except Exception:
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

        return Response(status=status.HTTP_200_OK)


class AccountDeleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            204: NO_CONTENT,
            401: UNAUTHORIZED,
        },
    )
    def delete(self, request):
        user = request.user

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: NO_CONTENT,
            401: UNAUTHORIZED,
        },
    )
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class CustomerListView(APIView):
    permission_classes = (IsStaff,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses={200: UserSerializer(many=True), 401: UNAUTHORIZED},
    )
    def get(self, request):
        customers = User.objects.filter(is_staff=False)
        return Response(self.serializer_class(customers, many=True).data)


class StaffViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Staff."""

    model = User
    queryset = User.objects.filter(is_staff=True, is_superuser=False)

    serializer_class = UserSerializer

    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: BAD_REQUEST,
            401: UNAUTHORIZED,
        },
    )
    def create(self, request):
        """Create View for Staff."""

        serializer = self.serializer_class(
            data=request.data, context={"is_staff": True}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: BAD_REQUEST,
            401: UNAUTHORIZED,
        },
    )
    def update(self, request, pk=None, *args, **kwargs):
        """Update View for Staff."""

        instance = self.get_object()

        serializer = self.serializer_class(
            instance, data=request.data, context={"is_staff": True}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
