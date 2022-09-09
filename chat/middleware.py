from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from firebase_admin import auth
from firebase_admin import credentials
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user(fire_token):

    try:
        decoded_token = auth.verify_id_token(fire_token)
        uid = decoded_token.get("uid")
        user = User.objects.get(id=uid)
        return user

    except User.DoesNotExist:
        return AnonymousUser()


class FirebaseAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            fire_token = (dict((x.split('=') for x in scope['query_string'].decode().split(
                "&")))).get('token', None)
        except ValueError:
            fire_token = None
        scope['user'] = AnonymousUser() if fire_token is None else await get_user(fire_token)
        return await super().__call__(scope, receive, send)
