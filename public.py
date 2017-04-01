from service.resources import LoginResource


def make_public_api(service):
    service.public_api.add_resource('/login', LoginResource())



