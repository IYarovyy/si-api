from typing import List

from quart import request, Blueprint, current_app
from quart_jwt_extended import jwt_required
from quart_schema import (validate_response, document_request)

from si_api.controllers.ctrl_models import Prediction, ErrorMsg, Predictions

controller = Blueprint('predict', __name__, url_prefix='/predict')

ALLOWED_EXTENSIONS = {'WAV', 'MP3', 'AAC', 'OGG', 'WMA', 'FLAC', 'AIFF', 'M4A', 'APE'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS


@controller.post('/')
@jwt_required
# @document_request()
@validate_response(Predictions, 200)
@validate_response(ErrorMsg, 400)
async def predict():
    files = await request.files
    res_predictions = Predictions(list())
    for name, file in files.items():
        if file and allowed_file(file.filename):
            predictions = await current_app.prediction_engine.analyze(file)
            res_predictions.predictions.append(Prediction(file=file.filename, prediction=list(predictions)))

    print(res_predictions)

    if len(res_predictions.predictions) == 0:
        return ErrorMsg("File not supplied"), 400
    else:
        return res_predictions, 200
