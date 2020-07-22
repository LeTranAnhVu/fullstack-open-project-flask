import os
from flask import Blueprint, jsonify, abort, request, send_from_directory
from main import app, db, Image
from main.helpers.type2type import str2bool
from main.helpers.upload_file import upload_file
import blurhash as blurhash_maker

import datetime
from main.config import URL_CONFIG, RESOURCE_CONFIG

blueprint = Blueprint('files', __name__)


def image_handler(saved_filepaths):
    imageModels = []
    for filepath in saved_filepaths:
        name = filepath.split('/')[-1]
        hash = ''
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'images', name), 'rb') as imagefile:
            hash = blurhash_maker.encode(os.path.join(
                app.config['UPLOAD_FOLDER'], 'images', name), x_components=4, y_components=3)
        imageModel = Image(name=name, blurhash=hash, url=filepath)
        db.session.add(imageModel)
        imageModels.append(imageModel)
    db.session.commit()
    # print([image.to_json() for image in imageModels])
    return {'data': [image.to_json() for image in imageModels]}, 201


# CRUD files
@blueprint.route(f'/{RESOURCE_CONFIG.PUBLIC_URL}/<string:resource_type>/<string:resource_name>')
def get_resource(resource_type, resource_name):
    allowed_resource = {'images', 'documents', 'css'}
    if (resource_type not in allowed_resource):
        abort(400, {'message': 'Restricted resource'})
    return send_from_directory(app.config['UPLOAD_FOLDER'], f'{resource_type}/{resource_name}')


@blueprint.route('/upload/<string:resource_type>', methods=['POST'])
def saved_files(resource_type):
    allowed_resource = {'images', 'documents', 'css'}
    if (resource_type not in allowed_resource):
        abort(400, {'message': 'Restricted resource'})
    if request.method == 'POST':
        try:
            file_list = request.files.getlist('files')
            if len(file_list) == False:
                abort(400, {'message': 'there is no file'})
            saved_filepaths = []
            for file in file_list:
                saved_filepaths.append(upload_file(file, resource_type))
            if (resource_type == 'images'):
                return image_handler(saved_filepaths)
            else:
                return {'message': 'upload successfully'}
        except Exception as e:
            print(e)
            abort(400, e)
