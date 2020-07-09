from main.config import RESOURCE_CONFIG
def allowed_file(filename):
    return filename.split('.')[-1] in RESOURCE_CONFIG.ALLOW_EXTENSION