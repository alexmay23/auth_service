import asyncio

from aiohttp import web
from asynclib.http.parser import use_schema, throwable
from webargs.aiohttpparser import use_args

from service.facade import UserFacade
from service.parser import Identity, Password
from service.schemes import AuthSchema


class BaseUserResource(object):
    def __init__(self):
        self.facade = UserFacade()


class LoginResource(BaseUserResource):

    @asyncio.coroutine
    @throwable
    @use_args({'identity': Identity(required=True), 'password': Password(required=True)})
    @use_schema(AuthSchema)
    def post(self, request, args):
        result = yield from self.facade.login(args['identity'], args['password'])
        return result