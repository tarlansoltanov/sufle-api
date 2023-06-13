from rest_framework import serializers

from ..models import Contact


class ContactWriteSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=list(Contact.TYPES_CHOICES), default=1)

    class Meta:
        model = Contact
        fields = ["name", "surname", "phone", "type", "message"]
