from django.db import models
from accounts.models import User
# Create your models here.

class Contact(models.Model):
    """
     contact model for storing unregistered users/user contacts
    """
    phone_no = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=False,default=None)
    spam = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserContact(models.Model):
    """
    Model to store contact of users in his phone book
    """
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user) + " --> " +  str(self.contact)


