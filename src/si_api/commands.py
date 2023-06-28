import asyncio
import re

import click
from quart import Quart
from quart_bcrypt import Bcrypt

from database import ConnectionPool
from services import user as user_service

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def register(app: Quart):
    def validate_email(ctx, param, value):
        if EMAIL_REGEX.fullmatch(value):
            return value
        else:
            raise click.BadParameter("Bad format of emai: " + value)

    async def add_user(email: str,
                       role: str,
                       password: str, app: Quart):
        app.db_pool = await ConnectionPool.get_pool(app)
        app.bcrypt = Bcrypt(app)
        return await user_service.add_user(email, role, password, app)

    @app.cli.command("create_user")
    @click.option('-e', '--email', type=click.UNPROCESSED, callback=validate_email, help="Users's email")
    @click.option('-r', '--role', type=click.Choice(['admin', 'common'], case_sensitive=False))
    @click.option('-p', '--password', prompt=True, help="User's password", hide_input=True,
                  confirmation_prompt=True)
    def create_user(email, role, password):
        click.echo("User with email:{email}, and role:{role} will be added.".format(email=email, role=role))
        asyncio.run(add_user(email, role, password, app))

    return app
