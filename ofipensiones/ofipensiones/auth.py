from typing import Optional, override

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication

import requests

JWT_SECRET = "UNSAFE+374eefc35ba1693bcf9663e091c3051493ff7d6ad0c6fd9c6fdb6a2f2"

class oauth_password(BaseBackend):
    @override
    def authenticate(self, request, username=None, password=None) -> Optional[User]:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        response = requests.post("http://auth/login", data=data)

        if response != 200:
            return None

        access_token = response.json().get("access_token")
        if access_token:
            user, _ = User.objects.get_or_create(username=username)
            return user

    @override
    def get_user(self, user_id) -> Optional[User]:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class token_auth(TokenAuthentication):
    keyword = "Bearer"

    @override
    def authenticate_credentials(self, key):
        pass
