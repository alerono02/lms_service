import re

from rest_framework.serializers import ValidationError


class LessonValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = dict(value).get(self.field)
        if not url.startswith('https://www.youtube.com/'):
            raise ValidationError("Not youtube link")