import json
import os
from typing import Optional

from quart import Quart, render_template
from quart_bcrypt import Bcrypt
from quart_cors import cors
from quart_jwt_extended import JWTManager
from quart_schema import (QuartSchema, Info)

from database import ConnectionPool
from si_api import commands
from si_api.controllers.auth import add_claims_to_access_token, add_claims_to_access_token, \
    user_identity_lookup
from si_api.controllers.auth import controller as auth_controller, check_if_token_in_blacklist
from si_api.controllers.person import controller as person_controller
from si_api.controllers.prediction import controller as prediction_controller
from si_api.controllers.user import controller as user_controller
from si_api.prediction.prediction_engine import PredictionEngine
from si_api.services import user as user_service
from si_api.files import get_full_path


# def run_evolutions(app: Quart):
#     if app.config['RUN_EVOLUTION']:
#         ev_dir = app.config['EVOLUTION_DIR']
#         db_url = app.config['DB_URL']
#         db_user = app.config['DB_USER']
#         db_pwd = app.config['DB_PWD']
#         ev_args = ['', db_url, db_user, db_pwd, ev_dir, '--skip=1']
#
#         evolutions.main(ev_args)


def create_app(o_mode: Optional[str]):
    mode = 'Development'
    if o_mode:
        mode = o_mode
    app = Quart(__name__, static_folder="assets")
    app.config.from_object(f"si_api.config.{mode}")
    app = cors(app, allow_origin="*")
    return app


mode = os.environ.get('SI_MODE')
app = create_app(mode)

app = commands.register(app)

# run_evolutions(app)

app.register_blueprint(user_controller)
app.register_blueprint(person_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(prediction_controller)


@app.before_serving
async def add_jwt_manager():
    app.jwt = JWTManager(app)
    app.jwt.user_identity_loader(user_identity_lookup)
    app.jwt.user_claims_loader(add_claims_to_access_token)
    app.jwt.token_in_blacklist_loader(check_if_token_in_blacklist)


@app.route("/")
async def index():
    manifest_path = get_full_path('si_api', 'manifest.json')
    with open(manifest_path) as manifest_file:
        manifest = json.load(manifest_file)
        print(manifest)
        return await render_template("index.html", manifest=manifest)


@app.before_serving
async def init():
    app.bcrypt = Bcrypt(app)
    QuartSchema(app,
                info=Info(title="Speaker Identifier", version=app.config['OPENAPI_VERSION']),
                servers=app.config['OPENAPI_SERVER'],
                security_schemes={
                    "MyBearer": {"type": "http", "scheme": "bearer"}
                })


@app.before_serving
async def init_prediction_engine():
    app.prediction_engine = PredictionEngine(
        app.config['PREDICT_MODEL_DIR'] + app.config['PREDICT_MODEL_DEFAULT'],
        app.config['PREDICT_MODEL_DIR'] + app.config['PREDICT_SCALER_DEFAULT']
    )


@app.before_serving
async def on_start():
    app.db_pool = await ConnectionPool.get_pool(app)


@app.after_serving
async def on_stop():
    await app.db_pool.close()


def run() -> None:
    app.run()
