# coding=utf-8

import phonenumbers
from asynclib.http.parser import String
from service.errors import InvalidIdentityError, PasswordTooShortError


class Identity(String):

    async def deserialize(self, value):
        value = await super(Identity, self).deserialize(value)
        if '@' in value:
            return value
        else:
            try:
                if value and value[0] != '+':
                    value = '+' + value
                number = phonenumbers.parse(value)
                if phonenumbers.is_valid_number(number):
                    return value
            except phonenumbers.NumberParseException:
                pass
        raise InvalidIdentityError()


class Password(String):

    async def deserialize(self, value):
        value = await super(Password, self).deserialize(value)
        if len(value) < 5:
            raise PasswordTooShortError()
        return value