import asyncio
import re

import click
from database import ConnectionPool
from quart import Quart
from services.user import UserService

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


class AddSuperuserCommandError(RuntimeError):
    def __init__(self, *args, **kwargs):
        pass


def register(app: Quart):
    def validate_email(ctx, param, value):
        if EMAIL_REGEX.fullmatch(value):
            return value
        else:
            raise click.BadParameter("Bad format of emai: " + value)

    async def add_user(email: str,
                       role: str,
                       password: str, app: Quart):
        user_service = UserService()
        app.db_pool = await ConnectionPool.get_pool(app)
        return await user_service.add_user(email, role, password, app)

    @app.cli.command("create_user")
    @click.option('-e', '--email', type=click.UNPROCESSED, callback=validate_email, help="Users's email")
    @click.option('-r', '--role', type=click.Choice(['chief', 'regular', 'operator'], case_sensitive=False))
    @click.option('-p', '--password', prompt=True, help="Users's password", hide_input=True,
                  confirmation_prompt=True)
    def create_user(email, role, password):
        click.echo(email)
        click.echo(role)
        click.echo(password)


        result = asyncio.run(add_user(email, role, password, app))

    return app
