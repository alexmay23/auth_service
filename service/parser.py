# coding=utf-8

import phonenumbers
from marshmallow import fields

from service.errors import InvalidIdentityError, PasswordTooShortError


class Identity(fields.String):

    def _serialize(self, value, attr, obj):
        return super(Identity, self)._serialize(value, attr, obj)

    def _deserialize(self, value, attr, data):
        value = super(Identity, self)._deserialize(value, attr, data)
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





class Password(fields.String):

    def _serialize(self, value, attr, obj):
        return super(Password, self)._serialize(value, attr, obj)

    def _deserialize(self, value, attr, data):
        value = super(Password, self)._deserialize(value, attr, data)
        if len(value) < 5:
            raise PasswordTooShortError()
        return value


# class Language(fields.String):
#
#     def _serialize(self, value, attr, obj):
#         return super(Language, self)._serialize(value, attr, obj)
#
#     def _deserialize(self, value, attr, data):
#         value = super(Language, self)._deserialize(value, attr, data)
#         available_languages = DynamicConfigDB().get_allowed_languages()
#         available_languages = list(map(lambda x: x.decode("utf-8"), available_languages))
#         if value not in available_languages:
#             raise LanguageNotAvailableError()
#         return value
#
#
# class Birthday(fields.Field):
#
#     def __init__(self, *args, **kwargs):
#         super(Birthday, self).__init__(*args, **kwargs)
#         self.format = "%Y-%m-%d"
#
#     def _serialize(self, value, attr, obj):
#         if value is None:
#             return None
#         return value.strftime(self.format)
#
#     def _deserialize(self, value, attr, data):
#         if value is None:
#             return None
#         date = datetime.datetime.strptime(value, self.format)
#         date.replace(hour=12, minute=0, second=0, tzinfo=datetime.timezone.utc)
#         return date