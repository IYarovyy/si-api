from quart import Quart

from src.si_api.controllers.person import controller as person_controller
from src.si_api.controllers.user import controller as user_controller

app = Quart(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(person_controller)

print(app.url_map)


def run() -> None:
    app.run()
