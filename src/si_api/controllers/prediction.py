from quart import request, Blueprint, current_app
from quart.datastructures import FileStorage
from quart_jwt_extended import jwt_required

controller = Blueprint('predict', __name__, url_prefix='/predict')

ALLOWED_EXTENSIONS = {'WAV', 'MP3', 'AAC', 'OGG', 'WMA', 'FLAC', 'AIFF', 'M4A', 'APE'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS


@controller.post('/')
@jwt_required
async def predict():
    files = await request.files
    prediction = []
    for name, file in files.items():
        if file and allowed_file(file.filename):
            print(type(file))
            [data, rate] = await current_app.prediction_engine.analize(file)

            print(f'Processing {file.filename}: {rate}')
            prediction.append({"name": file.filename, "len": rate})

    if len(prediction) == 0:
        ret = {"msg": "File not supplied"}
        return ret, 400
    else:
        return prediction, 200
