from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['phone_no', 'name', 'email', 'password', 'password2' ]

    def validate_phone_no(self, phone_no):
        # validate phone number if it contains any characters other than digits
        if not phone_no.isdigit():
            raise serializers.ValidationError({"phone_no" : "Not a valid phone number"})
        return phone_no

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            phone_no=validated_data['phone_no'],
            name=validated_data['name'],
        )
        if 'email' in validated_data:
            user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        return user