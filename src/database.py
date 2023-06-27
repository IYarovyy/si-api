import asyncpg

from quart import Quart


class ConnectionPool:
    _POOL = None

    def __init__(self):
        if ConnectionPool._POOL is not None:
            raise Exception("This class is a singleton!")
        else:
            ConnectionPool._POOL = self

    @classmethod
    async def get_pool(cls, app: Quart):
        db_url = app.config['DB_URL']
        # TODO Make db url properly
        db_user = app.config['DB_USER']
        db_pwd = app.config['DB_PWD']

        print("===== {} ====".format(cls._POOL))
        if cls._POOL is None:
            cls._POOL = await asyncpg.create_pool(db_url, command_timeout=60)
        return cls._POOL
