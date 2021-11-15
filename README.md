# Hotel-Backend

backend for Hotel web application. developed using django-rest-framework for Data structure and algorithms project

## Quickstart

Use the packet manager [pip](https://pip.pypa.io/en/stable/) to install virtual environment

```bash
pip install virtualenv
```

create virtual environment

```bash
virtualenv venv
```

activate virtual environment

```bash
venv\scripts\activate
```

install dependencies

```bash
pip install django djangorestframework django-cors-headers djangorestframework_simplejwt djongo
```
## Requirement

we're using mongodb as our database so create a database called *hoteldb*

then you can make migrations to the database and migrate using

```bash
py manage.py makemigrations
py manage.py migrate
```

lastly, run the backend server using

```bash
py manage.py runserver
```

## API

* `api/room/` listing the rooms and creating room
...Methods allowed : GET, POST
* `api/room/<int:pk>/` get the specified id room, update and delete
...Methods allowed : GET, PUT, DELETE
* `api/roomtype/` listing the room typesand create
...Methods allowed : GET, PUT, POST
* `api/roomtype/<int:pk>` update the specified room type
...Methods allowed : PUT
* `api/room/sort/` listing all the room after sorted in the specified method
...Methods allowed : GET
