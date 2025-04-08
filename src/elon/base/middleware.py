
import logging
import time
from datetime import datetime
from os.path import exists as pathexists
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware as BaseSessionMiddleware
from django.core.exceptions import ImproperlyConfigured
from rest_framework_simplejwt.tokens import RefreshToken


def _parse_key(key):
    def _load_key(k):
        if pathexists(k):
            k = open(k, 'rb').read()
        return k

    if isinstance(key, tuple):
        # Key pair.
        return _load_key(key[0]), _load_key(key[1]), 'RS256'

    key = _load_key(key)
    return key, key, 'HS256'


def _parse_fields(fields):
    "Parse and validate field definitions."
    snames, lnames = [], []

    for i, field in enumerate(fields):
        # Transform field in 3-tuple.
        if isinstance(field, tuple):
            if len(field) == 2:  # (attrname, sname)
                field = (field[0], field[1], field[1])

            elif len(field) == 1:  # (attrname)
                field = (field[0], field[0], field[0])

        else:  # attrname
            field = (field, field, field)

        # Collect all snames and lnames for uniqueness check.
        snames.append(field[1])
        lnames.append(field[2])

        # Validate that "sk" is not used, we use that for the session key.
        if field[1] == SESSION_FIELD:
            raise ImproperlyConfigured(
                'Short name "%s" is reserved for session field. Use '
                'DJANGO_SESSION_JWT["SESSION_FIELD"] to specify another '
                'value.' % SESSION_FIELD)

        if len(field) != 3:
            raise ImproperlyConfigured(
                'DJANGO_SESSION_JWT["FIELDS"] should be a list of 3-tuples.')

        fields[i] = field

    if len(snames) != len(set(snames)):
        raise ImproperlyConfigured(
            'DJANGO_SESSION_JWT["FIELDS"] short names are not unique')

    if len(lnames) != len(set(lnames)):
        raise ImproperlyConfigured(
            'DJANGO_SESSION_JWT["FIELDS"] long names are not unique')

    return fields



SIMPLE_JWT = getattr(settings, 'SIMPLE_JWT', {})
SESSION_FIELD = SIMPLE_JWT.get('SESSION_FIELD', 'sk')
KEY, PUBKEY, ALGO = _parse_key(SIMPLE_JWT.get('SIGNING_KEY', settings.SECRET_KEY))
FIELDS = _parse_fields(SIMPLE_JWT.get('FIELDS', []))
EXPIRES = SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', None)
# SESSION_ID = {}
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def rgetattr(obj, name):
    "Recursive getattr()."
    names = name.split('.')
    for n in names:
        obj = getattr(obj, n)
    return obj


def verify_jwt(blob):
    """
    Verify a JWT and return the session_key attribute from it.
    """
    try:
        fields = jwt.decode(blob, PUBKEY, algorithms=[ALGO])
    except (DecodeError, ExpiredSignatureError):
        return {}   

    return fields


def create_jwt(user, session_key, expires=None):
    """
    Create a JWT for the given user containing the configured fields.
    """
    # SESSION_ID['sk'] = session_key

    refresh = RefreshToken.for_user(user)
    refresh['sk'] = session_key
    return str(refresh.access_token)



def convert_cookie(cookies, user):
    cookie = cookies[settings.SESSION_COOKIE_NAME]
    cookies[settings.SESSION_COOKIE_NAME] = create_jwt(
        user, cookie.value, EXPIRES)


class SessionMiddleware(BaseSessionMiddleware):
    """
    Extend django.contrib.sessions middleware to use JWT as session cookie.
    """

    def process_request(self, request):
        session_jwt = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        fields = verify_jwt(session_jwt)
        session_key = fields.pop(SESSION_FIELD, None)
        request.session = self.SessionStore(session_key)
        if fields:
            request.session['jwt'] = fields

    def process_response(self, request, response):
        if not request.user.is_authenticated:
            User = get_user_model()
            try:
                user_id = request.session['jwt']['user_id']
                user = User.objects.get(id=user_id)
            except (KeyError, User.DoesNotExist):
                user = None
        else:
            user = request.user

        super(SessionMiddleware, self).process_response(request, response)

        expires = getattr(request, 'session', {}).get('jwt', {}).get('exp', None)
        halftime = time.mktime((datetime.utcnow() + EXPIRES).timetuple())
        halflife = expires and expires <= halftime

        if not halflife and not request.session.modified and \
           not settings.SESSION_SAVE_EVERY_REQUEST:
            return response

        try:
            convert_cookie(response.cookies, user)
        except (KeyError, AttributeError):
            pass

        return response