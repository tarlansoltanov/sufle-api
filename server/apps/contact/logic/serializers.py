from rest_framework import serializers

from ..models import Contact


class ContactSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=list(Contact.TYPES_CHOICES), default=1)

    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "surname",
            "phone",
            "type",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["type"] = instance.get_type_display()

        return data
