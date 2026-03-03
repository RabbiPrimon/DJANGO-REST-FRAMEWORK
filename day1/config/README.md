# Day 1 - Django REST Framework (Todo API)

This project is a beginner DRF setup with a simple Todo API and Django admin integration.

## Project Path
`day1/config`

## Features
- Todo model (`title`, `is_done`, `created_at`)
- DRF serializer using `ModelSerializer`
- API endpoint for todo list
- Django admin panel with `TodoAdmin`

## API Endpoint
- `GET /api/todos/`

Example:
`http://127.0.0.1:8000/api/todos/`

## Admin Panel
- URL: `http://127.0.0.1:8000/admin/`
- Superuser username: `admin`

## Setup
```bash
cd "e:\Md-Rabbi-Islam\DJANGO-REST-FRAMEWORK\day1\config"
python -m venv Env
.\Env\Scripts\activate
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

## Create Superuser
```bash
python manage.py createsuperuser
```

## Today Learning Notes
Detailed notes:
- `DAY1_LEARNING.md`
