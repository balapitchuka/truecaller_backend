from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer


# Create your views here.
class SignUpView(APIView):
    """
    Signup view for  new user registration
    Signing up requires a phone number and name of the user as mandatory fields

    Sample Payload to Send for User Registration
        {
            "phone_no" : "91 44444",
            "password" : "B123@111",
            "password2" : "B123@111",
            "name" : "priya"
        } 
    """
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            # user validation success
            serializer.save()
            data = {
                "message" : "User got Registered successfully"
            }
            return Response(data=data)
        else:
            # user validation failed
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(serializer.errors, status=status_code)
    
