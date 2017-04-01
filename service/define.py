from collections import namedtuple

_user_identity_type = namedtuple('USER_IDENTITY_TYPE', ('email', 'phone'))
USER_IDENTITY_TYPE = _user_identity_type('email', 'phone')