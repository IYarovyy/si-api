import enum
from typing import Optional

from quart import Quart
from quart_bcrypt import Bcrypt
from si_api.repositories import user as user_repository


class UserRoles(enum.Enum):
    admin = 0
    common = 10


class UserService():
    __bcrypt = None

    def get_bcrypt(self, app: Quart):
        if self.__bcrypt is None:
            self.__bcrypt = Bcrypt(app)
        return self.__bcrypt

    async def add_user(self,
                       email: str,
                       role: str,
                       password: str, app: Quart):

        data = {
            "email": email,
            "urole": role,
            "password": self.get_bcrypt(app).generate_password_hash(password).decode('utf-8')
        }

        return await user_repository.add_user(data, app)

    async def add(self,
                  email: str,
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

    async def get_by_id(self, user_id: int):
        return user_repository.find_user_by_id(user_id)

    async def get_by_email(self, email: str):
        return user_repository.find_user_by_email(email)
