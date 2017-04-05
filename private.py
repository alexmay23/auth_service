from service.facade import UserFacade


def make_private_api(api):
    user_facade = UserFacade()
    api.register_endpoint('login_by_jwt', user_facade.login_by_jwt)



