import asyncio

from asynclib.http.auth_lib import parse_token
from asynclib.http.marshall import dump, OKSchema
from asynclib.http.parser import parse_args, String
from aiohttp.web import Request
from service.facade import UserFacade
from service.parser import Identity, Password
from service.schemes import AuthSchema, UserSchema


class BaseUserResource(object):
    def __init__(self):
        self.facade = UserFacade()

    async def parse_user(self, request):
        user = await self.facade.login_by_jwt(parse_token(request))
        return user


auth_args = {'identity': Identity(required=True), 'password': Password(required=True)}


def auth_resp(auth):
    return dump(AuthSchema, {'user': auth[0], 'token': auth[1]})


class LoginResource(BaseUserResource):

    async def post(self, request):
        args = await parse_args(await request.json(), arg_map=auth_args)
        result = await self.facade.login(args['identity'], args['password'])
        return auth_resp(result)


class RegisterResource(BaseUserResource):

    async def post(self, request):
        args = await parse_args(await request.json(), arg_map=auth_args)
        result = await self.facade.register(args['identity'], args['password'])
        return auth_resp(result)


update_args = {'timezone': String(), 'locale': String()}


class UserResource(BaseUserResource):

    async def get(self, req):
        user = await self.facade.login_by_jwt(parse_token(req))
        return dump(UserSchema, user)

    async def put(self, req):
        args = await parse_args(await req.json(), update_args)
        user = await self.parse_user(req)
        user = await self.facade.update_user(user, args)
        return dump(UserSchema, user)


class VerifyIdentityResource(BaseUserResource):

    async def put(self, req):
        """

        :type req: Request
        """
        user = await self.parse_user(req)
        return self.facade.verify_identity(user, req.match_info.get('identity_id'), req.match_info.get('context'))


class SendVerificationContextResource(BaseUserResource):

    async def put(self, req):
        user = await self.parse_user(req)
        return self.facade.send_verification_context(user, req.match_info.get('identity_id'))


ok = dump(OKSchema, {'ok': True})


class ForgotResource(BaseUserResource):

    async def post(self, req):
        args = await parse_args(await req.json(), {'identity': Identity(required=True),
                                             'restore_hash': String(required=True),
                                             'password': Password(required=True)})
        result = await self.facade.restore_password(identity=args['identity'],
                                     restore_hash=args['restore_hash'], password=args['password'])
        return auth_resp(result)

    async def put(self, req):
        args = await parse_args(await req.json(), {'identity': Identity(required=True)})
        await self.facade.send_forgot_password_token(args['identity'])
        return ok