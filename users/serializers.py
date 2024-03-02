from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели пользователя.

        Attributes:
            id (int): Уникальный идентификатор пользователя.
            email (str): Адрес электронной почты пользователя.
            first_name (str): Имя пользователя.
            last_name (str): Фамилия пользователя.
            avatar (str): Путь к изображению профиля пользователя.
            phone (str): Номер телефона пользователя.
            city (str): Город пользователя
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'avatar', 'phone', 'city']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


