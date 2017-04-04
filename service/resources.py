import asyncio

from asynclib.http.marshall import dump
from asynclib.http.parser import parse_args

from service.facade import UserFacade
from service.parser import Identity, Password
from service.schemes import AuthSchema


class BaseUserResource(object):
    def __init__(self):
        self.facade = UserFacade()


auth_args = {'identity': Identity(required=True), 'password': Password(required=True)}


class LoginResource(BaseUserResource):

    async def post(self, request):
        args = await parse_args(await request.json(), arg_map=auth_args)
        user, token = await self.facade.login(args['identity'], args['password'])
        return dump(AuthSchema, {'user': user, 'token': token})


class RegisterResource(BaseUserResource):

    async def post(self, request):
        args = await parse_args(await request.json(), arg_map=auth_args)
        user, token = await self.facade.register(args['identity'], args['password'])
        return dump(AuthSchema, {'user': user, 'token': token})