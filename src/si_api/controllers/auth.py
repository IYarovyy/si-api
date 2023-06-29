from quart import request, Blueprint
from quart_jwt_extended import (
    create_access_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
)

from si_api.services import user as user_service
from si_api.services.user import AuthorizationException
from dataclasses import dataclass
from quart_schema import QuartSchema, validate_request, validate_response

controller = Blueprint('auth', __name__, url_prefix='/auth')


class UserObject:
    def __init__(self, email, role):
        self.email = email
        self.role = role


def add_claims_to_access_token(user):
    return {"role": user.role}


def user_identity_lookup(user):
    return user.email


blacklist = set()


def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist


@dataclass
class LoginData:
    email: str
    password: str


@controller.post('/login')
@validate_request(LoginData)
async def login(data: LoginData):
    try:
        user_data = await user_service.check_password(data.email, data.password)
        if user_data:
            user = UserObject(email=user_data['email'], role=user_data['urole'])
            access_token = create_access_token(identity=user)
            ret = {"access_token": access_token}
            return ret, 200
    except AuthorizationException as e:
        return {"msg": e.message}, 401


@controller.post("/refresh")
@jwt_refresh_token_required
async def refresh():
    current_user = get_jwt_identity()
    ret = {"access_token": create_access_token(identity=current_user)}
    return ret, 200


# Endpoint for revoking the current users access token
@controller.delete("/logout")
@jwt_required
async def logout():
    jti = get_raw_jwt()["jti"]
    blacklist.add(jti)
    return {"msg": "Successfully logged out"}, 200


# Endpoint for revoking the current users refresh token
@controller.delete("/logout2")
@jwt_refresh_token_required
async def logout2():
    jti = get_raw_jwt()["jti"]
    blacklist.add(jti)
    return {"msg": "Successfully logged out"}, 200
