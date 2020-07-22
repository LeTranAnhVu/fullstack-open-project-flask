import os
from flask import abort
from main.helpers.allowfile2upload import allowed_file
from main.config import RESOURCE_CONFIG
from werkzeug.utils import secure_filename
from main import app


def _make_fileurl(filename, resource_type) -> str:
    return os.path.join(RESOURCE_CONFIG.PUBLIC_URL, resource_type, filename)


def upload_file(file, resource_type) -> str:
    try:
        if (file.filename == "") or (not allowed_file(file.filename)):
            print('no name or no resource')
            abort(400, {'message': 'there is no image or invalid resource'})

        saved_filename = secure_filename(file.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], resource_type, saved_filename)

        # save
        file.save(saved_path)

        return _make_fileurl(saved_filename, resource_type)

    except Exception:
        abort(500, {'message': 'Cannot upload resource'})
