# Hotel-Backend

Backend for Hotel web application. Developed using django-rest-framework for Data Structure and Algorithms project. Deployed to Heroku and using MongoDB as our main database.

## Quickstart

Use the packet manager [pip](https://pip.pypa.io/en/stable/) to install virtual environment

```bash
pip install virtualenv
```

Create virtual environment

```bash
virtualenv venv
```

Activate virtual environment

```bash
venv\scripts\activate
```

Install dependencies

```bash
pip install django djangorestframework django-cors-headers djangorestframework_simplejwt djongo
```

## Requirement

We're using mongodb as our database so create a database called **hoteldb**

then you can make migrations to the database and migrate using

```bash
py manage.py makemigrations
py manage.py migrate
```

Lastly, run the backend server using

```bash
py manage.py runserver
```

## API

- `api/room/` listing the rooms and creating room  
   Methods allowed : GET, POST
- `api/room/<int:pk>/` get the specified id room, update and delete  
   Methods allowed : GET, PUT, DELETE
- `api/roomtype/` listing the room typesand create  
   Methods allowed : GET, PUT, POST
- `api/roomtype/<int:pk>/` update the specified room type  
   Methods allowed : PUT
- `api/room/sort/` listing all the room after sorted in the specified method  
   Methods allowed : GET
- `api/register/` registrations api (username and password needed)  
   Methods allowed : POST
- `api/user/` getting user information by using jwt token as Authentication  
   Methods allowed : GET
- `api/token` getting authentication  
   Methods allowed : POST
- `api/room/book/<int:pk>/` perform booking action to the room  
   Methods allowed : POST
- `api/room/check/date/` update all rooms by check today date to the exp_date  
   Methods allowed : GET
