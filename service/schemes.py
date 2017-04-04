from asynclib.http.marshall import Nested, MongoId
from asynclib.http.marshall import Schema
from asynclib.http.marshall import fields


class UserIdentitySchema(Schema):
    uid = fields.String()
    verified = fields.Boolean()
    type = fields.String()
    value = fields.String()


class UserSchema(Schema):
    _id = MongoId()
    name = fields.String(allow_none=True)
    timezone = fields.String(allow_none=True)
    locale = fields.String(allow_none=True)
    uid = fields.Integer()
    identities = Nested(UserIdentitySchema, many=True)


class AuthSchema(Schema):
    user = Nested(UserSchema)
    token = fields.String()
