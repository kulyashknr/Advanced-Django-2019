import os
from django.core.exceptions import ValidationError

ALLOWED_EXTS = ['.jpg', '.png']


def validate_file_size(value):
    if value.size > 2000000:
        raise ValidationError('max file size: 2Mb')


def validate_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in ALLOWED_EXTS:
        raise ValidationError(f'not allowed file ext, allowed: {ALLOWED_EXTS}')