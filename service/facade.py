import hashlib

import jwt
from asynclib.amqp.client import AMQPClient
from asynclib.utils.functions import random_with_N_digits
from bson import ObjectId

from service import define
from service.db import UserDBManager
from service.errors import WrongIdentityPasswordError, WrongTokenError, IdentityAlreadyExistsError, NoIdentityError, \
    AccessDeniedError, RestoreHashNotEqualError, NewPasswordIsEqualOldError
from service.instances import config
from service.lib import validate_password_hash





class UserFacade(object):

    def __init__(self):
        self.user_db = UserDBManager()

    async def login(self, identity, password):
        user = await self.user_db.get_by_identity(identity)
        if user is None or not validate_password_hash(password, user['password']):
            raise WrongIdentityPasswordError()
        return user, self.get_token(user)

    async def login_by_jwt(self, token):
        if token is None:
            raise WrongTokenError()
        payload = jwt.decode(token, verify=False)
        result = await self.user_db.get_by_id(ObjectId(payload['_id']))
        if result is None:
            raise WrongTokenError()
        if not self.validate_token(token, result):
            raise WrongTokenError()
        return result

    def get_token(self, user):
        """
        @type user: dict
        """
        data = {'_id': str(user['_id'])}
        secret_key = config.get('SECRET') + user['secret']
        return jwt.encode(data, secret_key, algorithm='HS256').decode('utf-8')

    def validate_token(self, token, user):
        """
        @rtype : bool
        @type user:dict
        """
        try:
            return jwt.decode(token, config.get('SECRET') + user['secret'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False

    async def register(self, identity, password):
        res = await self.user_db.get_by_identity(identity)
        if res is not None:
            raise IdentityAlreadyExistsError()
        user = await self.user_db.create(identity, self.what_is_identity(identity), password)
        return user, self.get_token(user)

    def what_is_identity(self, identity):
        if '@' in identity:
            return define.USER_IDENTITY_TYPE.email
        return define.USER_IDENTITY_TYPE.phone

    async def verify_identity(self, user, uid, verification_context):
        identity = await self.get_identity(uid, user)
        if identity.get('verification_context') == verification_context:
            await self.user_db.verify(uid)

    def identity_in_user(self, uid, user):
        try:
            return [i for i in user['identities'] if i['uid'] == uid][0]
        except IndexError:
            return None

    def check_identity_user(self, identified_user, user):
        if identified_user['_id'] != user['_id']:
            raise AccessDeniedError()

    async def send_verification_context(self, user, uid):
        identity = await self.get_identity(uid, user)
        verification_context = random_with_N_digits(6)
        await self.user_db.create_verification_context(uid, verification_context)
        await self.send_context_to_identity(identity, verification_context)

    async def get_identity(self, uid, user):
        identified_user = await self.user_db.get_by_identity(uid)
        if identified_user is None:
            raise NoIdentityError()
        self.check_identity_user(identified_user, user)
        identity = self.identity_in_user(uid, user)
        return identity

    def create_forgot_hash(self, user):
        _hash_str = str(user['_id']) + hashlib.sha256('VERY_SECRET_SALT'.encode()).hexdigest() + user['password']
        value = hashlib.sha256(_hash_str.encode()).hexdigest()
        return value[-5:]

    async def send_forgot_password_token(self, identity):
        user = await self.user_db.get_by_identity(identity)
        if user is None:
            raise NoIdentityError()
        identity_obj = [i for i in user['identities'] if i['value'] == identity][0]
        identity_type_message_map = {
            define.USER_IDENTITY_TYPE.email: 'Restoration code: {}'.format(self.create_forgot_hash(user)),
            define.USER_IDENTITY_TYPE.phone: 'Restoration code: {}'.format(self.create_forgot_hash(user))
        }
        await self.send_value_to_identity(identity_obj, identity_type_message_map, 'FORGOT PASSWORD')

    async def restore_password(self, identity, restore_hash, password):
        user = await self.user_db.get_by_identity(identity)
        if identity is None:
            raise NoIdentityError()
        if restore_hash != self.create_forgot_hash(user):
            raise RestoreHashNotEqualError()
        if validate_password_hash(password, user['password']):
            raise NewPasswordIsEqualOldError()
        self.user_db.set_password(user['_id'], password)
        return user, self.get_token(user)

    async def send_context_to_identity(self, identity, context):
        identity_type_message_map = {
            define.USER_IDENTITY_TYPE.email: 'http://{}/user/{}/verify/{}/{}'.format(config.get('HOST'),
                                         str(identity['user_id']), str(identity['_id']), context),
            define.USER_IDENTITY_TYPE.phone: 'Verification code {}'.format(context)
        }
        await self.send_value_to_identity(identity, identity_type_message_map, 'Email Verification')

    async def send_value_to_identity(self, identity, identity_type_message_map, subject):
        async with AMQPClient('transport') as client:
            if identity['type'] == define.USER_IDENTITY_TYPE.email:
                client.publish('mail', [{'recipient': identity['value'],
                                         'message': identity_type_message_map[define.USER_IDENTITY_TYPE.email],
                                         'subject': subject}])
            else:
                client.publish('sms', [{'recipient': identity['value'],
                                        'message': identity_type_message_map[define.USER_IDENTITY_TYPE.phone]}])

    async def update_user(self, user, args):
        await self.user_db.update(user['_id'], **args)
        user.update(args)
        return user
