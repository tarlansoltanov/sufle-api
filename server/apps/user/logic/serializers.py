from rest_framework import serializers

from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "birth_date", "password"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "birth_date": {"required": False},
            "phone": {"required": False},
            "password": {"write_only": True},
        }

    def save(self):
        user = User(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
            phone=self.validated_data.get("phone", None),
            birth_date=self.validated_data.get("birth_date", None),
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "date_joined",
        ]

        read_only_fields = ["id", "date_joined"]
