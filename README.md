# Truecaller Documentation


## Environment Setup

Note: Windows10 platform is used for development, use equivalent commands for project setup for linux and macos
##### 1. Check Python Installation and Virtualenv package installation
```
# python version
> python --version
Python 3.9.0

# django version 
> python -m django --version
3.1.7

# Install virtualenv package for virtualenv creation
> python -m pip install virtualenv

Note: code is developed with 3.9.0 python  version
```

##### 2. Setup Virtual Environment for the project
```
Make sure you are inside the "truecaller_backend" folder on the same level where manage.py fil is present.


1. Create new python virtual environment for the project
> python -m virtualenv truecaller_env

2. Activate the virtual environment
> truecaller_env\Scripts\activate

```

##### 3. Install dependencies for the project
```
> python -m pip install -r requirements.txt
```

##### 4. Running development django server
```
> python  manage.py runserver
```

##### Notes
- For development, django builtin sqlite database is being used.
- Incase want to login to django admin interface for CRUD operations, you can use the following admin user already being created in the database provided with the project.
- credentials of the admin:
    ```
    Visit : http://127.0.0.1:8000/admin/

    Credentials:

    "phone_no" : "911234567890",
    "password" : "1234"
    ```

#####5. Loading sample data into database
```
Using django fixtures to load test data

Test data is being stored in json files in following place in project
1. "truecaller_backend\accounts\fixtures\contacts.json"


Run following commands to load sample data into project
> python manage.py loaddata contacts.json
```

## Truecaller API's

Following are the api's available in  truecaller backend
```
api/auth/login/
api/auth/register/
api/auth/token/refresh/
api/contacts/search_phone/<str:phone_no>/
api/contacts/search_name/<str:name>/
api/contacts/spam/
api/contacts/detail/
```


#####API Detailing:
**`api/auth/register/`**

* API is used for new user registration.
* **Http Verb** : post
```
http://127.0.0.1:8000/api/auth/register/

Sample Body:

{
    "phone_no" : "911244444234",
    "password" : "B123@111",
    "password2" : "B123@111",
    "name" : "Testuser"
}
```
<hr>

**api/auth/login/**

* API is used for login of already registered users
* **http verb** : post
```
http://127.0.0.1:8000/api/auth/login/

Request Body:

{
    "phone_no" : "911234567890",
    "password" : "B123@111"
}
```

On successfull Authentication with credentials, jwt tokens will be provided in response to the request. There are two tokens access and refresh.

**Note:** 
* By default, access tokens are set to valid for 1 hour
* Change the access token life time validity setting using settings.py file
    - **'ACCESS_TOKEN_LIFETIME'** : timedelta(minutes=60)

<hr>

**`api/auth/token/refresh/`**

* API to obtain a new access token whenever existing access token expires
* **http verb** : post
```
http://127.0.0.1:8000/api/auth/token/refresh/

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDU3NTk4OSwianRpIjoiNDJhNzIxMzkyMTA0NGY4MmFmNzgxNjE4NWM4ZTM3NTgiLCJ1c2VyX2lkIjoxfQ.x7Bx-chkdCJYes1G9d8UaZQAA5NWeyBpv4WZz5Z0itg"
}
```

<hr>

**api/contacts/search_phone/<str:phone_no>/**

* API to search for a user by using phone number
* **Http Verb** : get
* Authentication : Required
    * Header   "Authorization" : "Bearer \<AccessToken\>"

```
Sample Request:

http://127.0.0.1:8000/api/contacts/search_phone/901235908907/
```

<hr>

**api/contacts/search_name/<str:name>/**
* API to search for a user by using name
* **Http Verb** : get
* Authentication : Required
    * Header   "Authorization" : "Bearer \<AccessToken\>"

```
Sample Request:

http://127.0.0.1:8000/api/contacts/search_name/Dhoni/

```

<hr>

**api/contacts/spam/**
* API to mark a phone number as spam
* **Http Verb** : post
* Authentication : Required
    * Header   "Authorization" : "Bearer \<AccessToken\>"

```
http://127.0.0.1:8000/api/contacts/spam/

{
    "phone_no" : "901235908907"
}
```

<hr>

**api/contacts/detail/**
* API to get detail profile by click on one of the  search results
* **Http Verb** : post
* Authentication : Required
    * Header   "Authorization" : "Bearer \<AccessToken\>"

```
http://127.0.0.1:8000/api/contacts/detail/

{
    "phone_no" : "901235908907",
    "name" : "Mahendra Singh  Dhoni",
    "spam" : true
}

```



### Testing APIS Using POSTMAN Tool
```
1. Inside 'truecaller_backend' there is postman folder which consists of following file:
"TrueCaller API.postman_collection.json"

2. Go to postman tool and  import the file  into postman.
This will list all the apis developed as listed above.
```