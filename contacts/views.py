from accounts.models import User
from accounts.serializers import UserSerializer
from django.db.models import F
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from contacts.models import Contact, UserContact
from contacts.serializers import ContactSerializer


# Create your views here.
class UserSearchByName(APIView):
    """
    An Non-empty name is needed to search for user by name.
    
    The name will be searched and listed in following order
        1. Results which start with name provided
        2. Results which contain the name provided
    
    Authentication : Needed, Only Authenticated Users are allowed to search by name.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, name):
        data = None
        if name:
            data = []
            registered_users = User.objects.all().filter(name__istartswith=name)
            contact_users = Contact.objects.filter(name__istartswith=name)
            registered_users_contain = User.objects.all().filter(name__icontains=name).exclude(name__istartswith=name)
            contact_users_contain = Contact.objects.filter(name__icontains=name).exclude(name__istartswith=name)
            data = UserSerializer(registered_users, many=True).data
            data += ContactSerializer(contact_users, many=True).data
            data += UserSerializer(registered_users_contain, many=True).data
            data += UserSerializer(contact_users_contain, many=True).data
            status_code = status.HTTP_200_OK
        else:
            # bad request from user
            data = {
                "message" : "Name cannot be empty"
            }
            status_code = status.HTTP_400_BAD_REQUEST 
        
        return Response(data=data, status=status_code)
            

class UserSearchByPhone(APIView):
    """
    View for User Search using Phone number

    An Non-empty phone number is needed to search for user by phone number.
    
    The name will be searched and listed according to following criteria:
        1. If a registered user is present with the given number, he will be only be returned.
        2. In case step one is not succeded, then will list all the contacts matching with the 
           phone_number who are not registered 
     
    Authentication : Needed, Only Authenticated Users are allowed to search by phone number
    """
    permission_classes = (IsAuthenticated,)

    def  get(self, request, phone_no):
        data = []
        if phone_no and phone_no.isdigit():
            user = User.objects.filter(phone_no=phone_no)
            if user.exists():
                user = user.first()
                data = [
                    {
                        "name" : user.name,
                        "phone_no" : user.phone_no,
                        "spam" : user.spam
                    }
                ]
                status_code = status.HTTP_200_OK
            else:
                contacts = Contact.objects.filter(phone_no=phone_no)
                contact_serializer = ContactSerializer(contacts, many=True)
                data = contact_serializer.data
                status_code = status.HTTP_200_OK
        else:
            # bad request from user
            data = {
                "message" : "Invalid phone number"
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=status_code)

class Spam(APIView):
    """
    View to mark a user a spam

    A Nonempty phone number should be provided by the user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        phone_no = request.data.get("phone_no")
        if phone_no and phone_no.isdigit():
            user = User.objects.filter(phone_no=phone_no).update(spam=True)
            Contact.objects.filter(phone_no=phone_no).update(spam=True)
            data = {
                "message" : "phone number marked as spam successfully"
            }
            status_code = status.HTTP_200_OK
        else:
            data = {
                "message" : "Invalid phone number"
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=status_code)

class UserSearchDetail(APIView):
    """
    View to return detail user profile
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logged_user = request.user
        phone_no = request.data.get("phone_no")
        name = request.data.get("name")
        spam = request.data.get("spam")
        data = {
            "phone_no" : phone_no,
            "name" : name,
            "spam" : spam
        }
        if name and phone_no and phone_no.isdigit():
            user = User.objects.filter(phone_no=phone_no)
            if user.exists():
                contact = Contact.objects.filter(phone_no=phone_no, name__iexact=name, spam=spam)
                if contact.exists():
                    contact = contact.first()
                    user_contact = UserContact.objects.filter(user=logged_user, contact=contact)
                    if user_contact.exists():
                        # if user is a registerd one and user contact exists in his phonebook
                        # then also send the email
                        data['email'] = contact.email
            status_code = status.HTTP_200_OK
        else:
            # bad request from user
            data = {
                "message" : "Invalid phone number/name"
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data, status=status.HTTP_200_OK)
        




