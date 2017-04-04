import click

from service.instances import service, config
from private import make_private_api
from public import make_public_api


@click.group()
def commands():
    pass



@commands.command()
def run_private_api():
    make_private_api(service.private_api)
    service.run_private_api()


@commands.command()
@click.option('--host', default=config.get('HOST', '127.0.0.1'))
@click.option('--port', default=config.get('PORT', 5000))
def run_public_api(host, port):
    make_public_api(service.public_api)
    service.run_public_api(host, port)



if __name__ == '__main__':
    commands()




