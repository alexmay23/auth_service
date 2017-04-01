
from asynclib.service import ServiceConfig, Service
from asynclib.utils.config import Config

config = Config()

service_config = ServiceConfig(
    name='auth',
    mongo_url=config.get('MONGO_URL', '127.0.0.1'),
    amqp_host=config.get('AMQP_HOST', '127.0.0.1'),
    amqp_user=config.get('AMQP_USER', 'guest'),
    amqp_password=config.get('AMQP_PASSWORD', 'guest')
)


service = Service(config=service_config)