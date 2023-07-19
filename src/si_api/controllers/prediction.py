from quart import request, Blueprint, current_app
from quart_jwt_extended import jwt_required

controller = Blueprint('predict', __name__, url_prefix='/predict')

ALLOWED_EXTENSIONS = {'WAV', 'MP3', 'AAC', 'OGG', 'WMA', 'FLAC', 'AIFF', 'M4A', 'APE'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS


@controller.post('/')
@jwt_required
async def predict():
    files = await request.files
    form = await request.form
    print(request.headers)
    print(form.keys())
    print(files)
    res_predictions = []
    for name, file in files.items():
        if file and allowed_file(file.filename):
            print(type(file))
            predictions = await current_app.prediction_engine.analyze(file)

            res_predictions.append({"file": file.filename, "prediction": predictions})
            # predictions.append({"file": file.filename, "prediction": predictions})

    if len(res_predictions) == 0:
        ret = {"msg": "File not supplied"}
        return ret, 400
    else:
        return {"predictions": res_predictions}, 200
