from django.contrib.auth import authenticate

def authenticate_user(username, password):
    return authenticate(username=username, password=password)
