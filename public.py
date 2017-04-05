from service.resources import LoginResource, RegisterResource, UserResource, VerifyIdentityResource, \
    SendVerificationContextResource, ForgotResource


def make_public_api(api):
    api.add_resource('/login', LoginResource())
    api.add_resource('/register', RegisterResource())
    api.add_resource('/user', UserResource())
    api.add_resource('/user/identity/{identity_id}/verify/{context}', VerifyIdentityResource())
    api.add_resource('/user/identity/{identity_id}/send', SendVerificationContextResource())
    api.add_resource('/forgot', ForgotResource())



