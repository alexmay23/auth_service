from service.facade import UserFacade



async def auth_by_token(token):
    user_facade = UserFacade()
    user = await user_facade.login_by_jwt(token)
    return user