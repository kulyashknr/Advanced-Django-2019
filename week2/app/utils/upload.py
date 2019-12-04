import os
import shutil
from datetime import datetime


def task_document_path(instance, filename):
  return f'tasks/{filename}'


def task_delete_path(document):
    datetime_path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(datetime_path)