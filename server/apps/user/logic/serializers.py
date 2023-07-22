from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer definition for User."""

    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        """Meta definition for UserSerializer."""

        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "password",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        ]
        extra_kwargs = {
            "phone": {"required": False},
            "birth_date": {"required": False},
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        email = value.lower()

        if self.instance and self.instance.email == email:
            return email

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Bu email istifadədədir! Zəhmət olmasa başqa email daxil edin!"
            )

        return email

    def validate_phone(self, phone):
        if not phone:
            return None

        if phone == "":
            return None

        if self.instance and self.instance.phone == phone:
            return phone

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "Bu telefon istifadədədir! Zəhmət olmasa başqa telefon daxil edin!"
            )

        return phone

    def get_validation_exclusions(self):
        exclusions = super(UserSerializer, self).get_validation_exclusions()
        if self.instance:
            return exclusions + ["email"]
        return exclusions

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not data.get("is_staff", False):
            data.pop("is_staff")
            data.pop("is_superuser")

        return data

    def create(self, validated_data):
        """Create user."""

        is_staff = self.context.get("is_staff", False)
        is_superuser = self.context.get("is_superuser", False)

        if is_staff:
            user = User.objects.create_staff(**validated_data)

        elif is_superuser:
            user = User.objects.create_superuser(**validated_data)

        else:
            user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data, partial=False):
        """Update user."""

        if partial:
            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()
            return instance

        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
