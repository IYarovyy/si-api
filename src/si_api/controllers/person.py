from quart import request, Blueprint

controller = Blueprint('person', __name__, url_prefix='/person')


@controller.post('/')
async def echo():
    data = await request.get_json()
    return {"input": data, "extra": True}
