from django.contrib import admin

from contacts.models import UserContact, Contact
# Register your models here.

admin.site.register(UserContact)
admin.site.register(Contact)