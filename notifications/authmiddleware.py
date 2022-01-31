from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs

@database_sync_to_async
def get_user(user_id):
    try:
        token =  Token.objects.get(user_id=user_id)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        print(scope['path'].split('/')[3])
        scope['user'] = await get_user(int(scope['path'].split('/')[3]))

        return await self.app(scope, receive, send)
