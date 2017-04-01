from service.amqp import auth_by_token


def make_private_api(service):
    service.private_api.register_endpoint('auth_by_token', auth_by_token)



