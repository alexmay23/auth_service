from asynclib.http.error import BaseError


class ErrorCodes(object):
    TOO_SHORT_PASSWORD_ERROR = 'TOO_SHORT_PASSWORD_ERROR'
    INVALID_IDENTITY_ERROR = 'INVALID_IDENTITY_ERROR'
    USER_WRONG_TOKEN_ERROR = 'WRONG_TOKEN_ERROR'
    NO_IDENTITY_ERROR = 'NO_IDENTITY_ERROR'
    WRONG_IDENTITY_PASSWORD_ERROR = 'WRONG_IDENTITY_PASSWORD_ERROR'
    IDENTITY_ALREADY_EXISTS_ERROR = 'IDENTITY_ALREADY_EXISTS_ERROR'
    RESTORE_HASH_NOT_EQUAL_ERROR = 'RESTORE_HASH_NOT_EQUAL_ERROR'
    NEW_PASSWORD_IS_EQUAL_OLD_ERROR = 'NEW_PASSWORD_IS_EQUAL_OLD_ERROR'
    ACCESS_DENIED = 'ACCESS_DENIED'


class WrongTokenError(BaseError):
    def __init__(self):
        super(WrongTokenError, self).__init__(
            ErrorCodes.USER_WRONG_TOKEN_ERROR,
            'Wrong token error',
            401
        )


class PasswordTooShortError(BaseError):

    def __init__(self):
        super(PasswordTooShortError, self).__init__(
            ErrorCodes.TOO_SHORT_PASSWORD_ERROR,
            'Too short password error',
            400

        )


class InvalidIdentityError(BaseError):
    def __init__(self):
        super(InvalidIdentityError, self).__init__(
            ErrorCodes.INVALID_IDENTITY_ERROR,
            'Invadlid identity error',
            400
        )

class NoIdentityError(BaseError):
    def __init__(self):
        super(NoIdentityError, self).__init__(
            ErrorCodes.NO_IDENTITY_ERROR,
            'No identity error',
            403
        )


class IdentityAlreadyExistsError(BaseError):
    def __init__(self):
        super(IdentityAlreadyExistsError, self).__init__(
            ErrorCodes.IDENTITY_ALREADY_EXISTS_ERROR,
            'Identity already registered',
            403
        )


class WrongIdentityPasswordError(BaseError):
    def __init__(self):
        super(WrongIdentityPasswordError, self).__init__(
            ErrorCodes.WRONG_IDENTITY_PASSWORD_ERROR,
            'Wrong identity or password',
            403
        )


class RestoreHashNotEqualError(BaseError):

    def __init__(self):
        super(RestoreHashNotEqualError, self).__init__(
            ErrorCodes.RESTORE_HASH_NOT_EQUAL_ERROR,
            'Restore hash not equal error',
            403
        )


class NewPasswordIsEqualOldError(BaseError):

    def __init__(self):
        super(NewPasswordIsEqualOldError, self).__init__(
            ErrorCodes.NEW_PASSWORD_IS_EQUAL_OLD_ERROR,
            'New password is equal old error',
            403
        )


class AccessDeniedError(BaseError):

    def __init__(self):
        super(AccessDeniedError, self).__init__(
            ErrorCodes.ACCESS_DENIED,
            'Access denied',
            403
        )


