from service.resources import LoginResource, RegisterResource


def make_public_api(api):
    api.add_resource('/login', LoginResource())
    api.add_resource('/register', RegisterResource())



