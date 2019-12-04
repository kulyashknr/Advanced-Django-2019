import os
import shutil
from datetime import datetime


def article_image_path(instance, filename):
    return f'articles/{filename}'


def article_delete_path(document):
    datetime_path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(datetime_path)