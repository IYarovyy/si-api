from quart import request, Blueprint
from quart_jwt_extended import jwt_required

from si_api.controllers.decorators import admin_required
from si_api.services import user as user_service

controller = Blueprint('user', __name__, url_prefix='/user')


@controller.get('/')
@jwt_required
@admin_required
async def get_user():
    req_json = await request.get_json()
    email = req_json.get("email", None)
    if email:
        user_data = await user_service.get_by_email(email)
        return {"email": user_data['email']}, 200
    else:
        ret = {"msg": "User not found"}
        return ret, 404
