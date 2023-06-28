import enum
from typing import Optional

from asyncpg import Record
from quart import Quart, current_app

from si_api.repositories import user as user_repository


class AuthorizationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UserRoles(enum.Enum):
    admin = 0
    common = 10


async def add_user(email: str,
                   role: str,
                   password: str, app: Quart):
    data = {
        "email": email,
        "urole": role,
        "password": app.bcrypt.generate_password_hash(password).decode('utf-8')
    }

    return await user_repository.add_user(data, app)


async def add(email: str,
              password: str,
              urole: str,
              first_name: Optional[str] = None,
              second_name: Optional[str] = None,
              department: Optional[int] = None):
    data = {
        "email": email,
        "urole": urole,
        "password": password  # TODO Use bcrypt
        # "password": bcrypt.generate_password_hash(password).decode('utf-8')
    }
    if first_name:
        data['first_name'] = first_name
    if second_name:
        data['second_name'] = second_name
    if department:
        data['department'] = department

    return await user_repository.insert_user(data)


async def get_by_id(user_id: int):
    return user_repository.find_user_by_id(user_id)


async def get_by_email(email: str):
    return await user_repository.find_user_by_email(email)


async def check_password(email: str, password: str) -> Record:
    user_data = await get_by_email(email)
    if user_data:
        print("User data: {0}".format(user_data))
        pass_hash = user_data['password']
        if pass_hash:
            if current_app.bcrypt.check_password_hash(pass_hash, password):
                return user_data
            else:
                raise AuthorizationException('Wrong password')
        else:
            raise AuthorizationException('Password is absent for user: {user}'.format(user=email))
    else:
        raise AuthorizationException('User: {user} is absent in the DB'.format(user=email))
