from quart import request, Blueprint

controller = Blueprint('user', __name__, url_prefix='/user')


@controller.post('/')
async def echo():
    data = await request.get_json()
    return {"input": data, "extra": True}
