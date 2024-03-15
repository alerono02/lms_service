## LMS Service

---

## Запуск проекта:

> Запуск Jango проекта через **Run - "название проекта"**
> или командой **python manage.py runserver** 

### Настройка DRF в Docker

**Клонировать проект:**
> https://github.com/alerono02/lms_service.git

### Сборка без yaml файла

**Сборка докер образа:**
> docker build -t my-python-app .

**Запуск контейнера:**
> docker run my-python-app

<br>

### Сборка с yaml файлом

**Cоздание образа из Dockerfile:**
> docker-compose build

с запуском контейнера:
> docker-compose up --build

с запуском конктейнера в фоновом режиме:
> docker-compose up -d --build

**Запуск контейнера:**
> docker-compose up

---

## Описание:

> Реализовать платформу для онлайн-обучения. 
Разработка LMS-системы, в которой каждый желающий может размещать свои полезные материалы или курсы.

---

## Технологии:
- Python
- Django
- Django DRF
- PostgreSQL
- JWT
- django_filters
- Redis
- Celery
- Celery Beat
- Swagger
- Docker
- Docker Compose
- Unittest


---

## Реализация:

**Задание**

Создайте новый Django-проект, подключите DRF и внесите все необходимые настройки.

**Задание**

Создайте следующие модели:

`Пользователь`:

- все поля от обычного пользователя, но авторизацию заменить на email;
- телефон;
- город;
- аватарка.

`Курс`:

- название,
- превью (картинка),
- описание.

`Урок`:

- название,
- описание,
- превью (картинка),
- ссылка на видео.

**Задание**

Опишите CRUD для моделей курса и урока, но при этом для курса сделайте через ViewSets, а для урока — через Generic-классы.

Для работы контроллеров опишите простейшие сериализаторы.

```bash
Работу каждого эндпоинта необходимо проверять 
с помощью Postman.
Также на данном этапе работы мы не заботимся о безопасности 
и не закрываем от редактирования объекты и модели 
даже самой простой авторизацией.
```

**Задание**

Реализуйте эндпоинт для редактирования профиля любого пользователя на основе более привлекательного подхода для личного использования: Viewset или Generic.

**Задание**

Для модели курса добавьте в сериализатор поле вывода количества уроков.

**Задание**

Добавьте новую модель `Платежи` со следующими полями:

- пользователь,
- дата оплаты,
- оплаченный курс или урок,
- сумма оплаты,
- способ оплаты: наличные или перевод на счет.

Запишите в эту модель данные через инструмент фикстур или кастомную команду.

**Задание**

Для сериализатора модели курса реализуйте поле вывода уроков.

**Задание**

Настройте фильтрацию для эндпоинтов вывода списка платежей с возможностями:

- менять порядок сортировки по дате оплаты,
- фильтровать по курсу или уроку,
- фильтровать по способу оплаты.

**Задание**

Настройте в проекте использование JWT-авторизации и закройте каждый эндпоинт авторизацией.

**Задание**

Заведите группу модераторов и опишите для нее права работы с любыми уроками или курсами, но без возможности их удалять и создавать новые. Заложите функционал такой проверки в контроллеры.

**Задание**

Опишите права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть и редактировать только свои курсы и уроки.

```bash 
Заводить группы лучше через админку 
и не реализовывать для этого дополнительных эндпоинтов.
```

**Задание**

Для профиля пользователя введите ограничения, чтобы авторизованный пользователь мог просматривать любой профиль, но редактировать только свой. При этом при просмотре чужого профиля должна быть доступна только общая информация, в которую не входят: пароль, фамилия, история платежей.

**Задание**

Для сохранения уроков и курсов реализуйте дополнительную проверку на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.

То есть ссылки на видео можно прикреплять в материалы, а ссылки на сторонние образовательные платформы или личные сайты — нельзя.

**Задание**

Добавьте модель подписки на обновления курса для пользователя.

Вам необходимо реализовать эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.

При этом при выборке данных по курсу пользователю необходимо присылать признак подписки текущего пользователя на курс. То есть давать информацию, подписан пользователь на обновления курса или нет.

**Задание**

Реализуйте пагинацию для вывода всех уроков и курсов.

**Задание**

Напишите тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.

**Задание**

Подключить и настроить вывод документации для проекта. Убедиться, что каждый из реализованных эндпоинтов описан в документации верно, при необходимости описать вручную.

**Задание**

Подключить возможность оплаты курсов через https://stripe.com/docs/api.

Доступы можно получить напрямую из документации, а также пройти простую регистрацию по адресу https://dashboard.stripe.com/register.

Для работы с запросами вам понадобится реализовать обращение к эндпоинтам:

https://stripe.com/docs/api/payment_intents/create — создание платежа;
https://stripe.com/docs/api/payment_intents/retrieve — получение платежа.
Для тестирования можно использовать номера карт из документации:

https://stripe.com/docs/terminal/references/testing#standard-test-cards

```bash Подключение оплаты лучше всего рассматривать как обычную задачу подключения к стороннему API.
Основной путь: запрос на покупку → оплата. 
Статус проверять не нужно.
Каждый эквайринг предоставляет тестовые карты для работы 
с виртуальными деньгами.
```

**Задание**

Настройте проект для работы с Celery. Также настройте celery-beat для выполнения последующих задач.

**Задание**

Ранее вы реализовывали функционал подписки на обновление курсов. Теперь добавьте асинхронную рассылку писем пользователям об обновлении материалов курса.

**Задание**

С помощью celery-beat реализуйте фоновую задачу, которая будет проверять пользователей по дате последнего входа по полю 
`last_login` и, если пользователь не заходил более месяца, блокировать его с помощью флага `is_active`.
