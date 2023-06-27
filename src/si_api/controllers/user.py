from quart import request, Blueprint
from services import user as user_service

controller = Blueprint('user', __name__, url_prefix='/user')


@controller.post('/')
async def echo():
    data = await request.get_json()
    res = await user_service.add("email", "password", "chief")
    return {"input": data, "extra": True}
