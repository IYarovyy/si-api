import os
from typing import Optional

import commands as commands
import evolutions
from controllers.person import controller as person_controller
from controllers.user import controller as user_controller
from database import ConnectionPool
from quart import Quart
from services import user as user_service


# def run_evolutions(app: Quart):
#     if app.config['RUN_EVOLUTION']:
#         ev_dir = app.config['EVOLUTION_DIR']
#         db_url = app.config['DB_URL']
#         db_user = app.config['DB_USER']
#         db_pwd = app.config['DB_PWD']
#         ev_args = ['', db_url, db_user, db_pwd, ev_dir]
#
#         evolutions.main(ev_args)


def create_app(o_mode: Optional[str]):
    if o_mode is None:
        mode = 'Development'
    else:
        mode = o_mode
    app = Quart(__name__)
    app.config.from_object(f"config.{mode}")
    return app


mode = os.environ.get('SI_MODE')
app = create_app(mode)

app = commands.register(app)

# run_evolutions(app)

app.register_blueprint(user_controller)
app.register_blueprint(person_controller)
@app.before_serving
async def on_start():
    print("========== on start ==========")
    app.db_pool = await ConnectionPool.get_pool(app)


@app.after_serving
async def on_stop():
    await app.db_pool.close()


def run() -> None:
    app.run()
