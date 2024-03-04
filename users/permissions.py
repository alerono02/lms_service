from rest_framework.permissions import BasePermission
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from django.db import models


class IsOwner(BasePermission):
    """
        Права доступа для владельца.

        Владелец имеет право видеть и редактировать свои объекты, а также видеть и редактировать уроки и курсы, если он
        модератор.

        Attributes:
            message (str): Сообщение об ошибке, которое будет возвращено при отсутствии доступа.
    """
    message = "Вы не являетесь владельцем."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Moderator').exists():
            return True
        else:
            return False


