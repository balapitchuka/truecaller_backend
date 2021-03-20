from django.urls import path
from contacts.views import UserSearchByName, UserSearchByPhone, Spam, UserSearchDetail

urlpatterns = [
    # path('helloworld/', HelloWorld.as_view(), name='test-api'),
    path('search_phone/<str:phone_no>/', UserSearchByPhone.as_view(), name='search-phone'),
    path('search_name/<str:name>/', UserSearchByName.as_view(), name='search-name'),
    path('spam/', Spam.as_view(), name='spam-user'),
    path('detail/', UserSearchDetail.as_view(),  name='user-detail'),

]
