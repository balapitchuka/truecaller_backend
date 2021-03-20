from rest_framework import serializers

from accounts.models import User
from contacts.models import Contact

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['phone_no', 'name', 'spam']
