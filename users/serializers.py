from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model


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
            country (str): Страна, в которой проживает пользователь.
    """

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'avatar', 'phone', 'country']


class UserLoginSerializer(serializers.Serializer):
    """
        Сериализатор для аутентификации пользователя.

        Attributes:
            email (str): Адрес электронной почты пользователя.
            password (str): Пароль пользователя.

        Methods:
            validate(data): Проверяет переданные данные на наличие
                корректных учетных данных пользователя.

        Raises:
            serializers.ValidationError: Если учетные данные некорректны или отсутствуют.

        Returns:
            dict: Словарь с проверенными данными, включая объект пользователя (если успешно).
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
