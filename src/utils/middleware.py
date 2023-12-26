from urllib.parse import parse_qs
from channels.db import database_sync_to_async
import jwt

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from config import settings

User = get_user_model()


class SimpleJWTAuthentication:
    """
    Simple JWT token based authentication.

    Clients should authenticate by passing the token in the Authorization header.
    For example:

        Authorization: Bearer <token>
    """

    def __init__(self):
        self.jwt_auth = JWTTokenUserAuthentication()

    def authenticate(self, token):
        user = self.get_user_from_token(token)

        if not user or not user.is_active:
            return AnonymousUser(), None

        return user

    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
            user_id = payload['user_id']
            return User.objects.get(id=user_id)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(_("Token has expired."))
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(_("Invalid token."))
        except User.DoesNotExist:
            return None


@database_sync_to_async
def get_user(scope):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    # postpone model import to avoid ImproperlyConfigured error before Django
    # setup is complete.
    from django.contrib.auth.models import AnonymousUser

    if "token" not in scope:
        raise ValueError(
            "Cannot find token in scope. You should wrap your consumer in "
            "TokenAuthMiddleware."
        )
    token = scope["token"]
    user = None
    try:
        auth = SimpleJWTAuthentication()
        user = auth.authenticate(token)
    except AuthenticationFailed:
        pass
    return user or AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware that takes a token from the query string and authenticates via
    JWT tokens.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded_data)
            scope["token"] = token
            scope["user"] = await get_user(scope)

        return await self.app(scope, receive, send)