# Day 1 Project Documentation: Django REST Framework Todo API

This directory contains a simple Todo API built with Django and Django REST Framework (DRF), plus Django Admin support for managing records from the browser.

## 1. Project Overview

- Project root (for this app): `day1/config`
- Frameworks:
  - Django
  - Django REST Framework
- Database:
  - SQLite (`db.sqlite3`)
- App name:
  - `api`

### Implemented Features

- `Todo` model with:
  - `title`
  - `is_done`
  - `created_at`
- Separate API endpoints for pending and completed todos
- Django admin integration with filter/search/list columns

## 2. Directory Structure

```text
day1/config/
  manage.py
  db.sqlite3
  config/
    settings.py
    urls.py
  api/
    models.py
    serializers.py
    views.py
    urls.py
    admin.py
    migrations/
```

## 3. Environment and Installation

Run from:

```bash
cd "e:\Md-Rabbi-Islam\DJANGO-REST-FRAMEWORK\day1\config"
```

### Create and activate virtual environment (Windows PowerShell)

```bash
python -m venv Env
.\Env\Scripts\activate
```

### Install dependencies

```bash
pip install django djangorestframework
```

### Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Configuration Notes

From `config/settings.py`:

- `INSTALLED_APPS` includes:
  - `rest_framework`
  - `api`
- `DEBUG=True` (development mode)
- `ALLOWED_HOSTS=[]` (default local setup)
- Database uses SQLite

## 5. Data Model

File: `api/models.py`

```python
class Todo(models.Model):
    title = models.CharField(max_length=120)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### Field Description

- `title`: short text for task title
- `is_done`: completion status (`True`/`False`)
- `created_at`: auto timestamp when record is created

## 6. Serializer

File: `api/serializers.py`

```python
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
```

This serializer exposes all model fields in API response.

## 7. API Layer

### View

File: `api/views.py`

```python
@api_view(['GET'])
def todo_list(request):
    todos = Todo.objects.filter(is_done=False).order_by('-created_at')
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def done_todo_list(request):
    todos = Todo.objects.filter(is_done=True).order_by('-created_at')
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)
```

### URLs

App urls (`api/urls.py`):

```python
urlpatterns = [
    path('todos/', todo_list),
    path('done-todos/', done_todo_list),
]
```

Project urls (`config/urls.py`):

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

### Available Endpoints

- `GET /api/todos/` -> only pending (`is_done=False`) todos
- `GET /api/done-todos/` -> only completed (`is_done=True`) todos

Example local URL:

- `http://127.0.0.1:8000/api/todos/`
- `http://127.0.0.1:8000/api/done-todos/`

### Example Response

```json
[
  {
    "id": 1,
    "title": "Learn Django Admin",
    "is_done": false,
    "created_at": "2026-03-05T09:31:16.690909Z"
  }
]
```

## 8. Django Admin

File: `api/admin.py`

```python
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_done", "created_at")
    list_filter = ("is_done",)
    search_fields = ("title",)
```

### Admin Access

- URL: `http://127.0.0.1:8000/admin/`

### Create Superuser

```bash
python manage.py createsuperuser
```

## 9. Run the Server

```bash
python manage.py runserver
```

Then visit:

- API: `http://127.0.0.1:8000/api/todos/`
- Admin: `http://127.0.0.1:8000/admin/`

## 10. Quick Validation Commands

### Run Django checks

```bash
python manage.py check
```

### Run tests

```bash
python manage.py test
```

Note: currently no automated test cases are implemented (`0 tests`).

## 11. Common Troubleshooting

### Problem: `404` on `/api/todos/`

- Ensure server is running from `day1/config`
- Ensure URL includes trailing slash: `/api/todos/`

### Problem: response does not look filtered

- `/api/todos/` should return only pending items
- `/api/done-todos/` should return only completed items
- Verify test data has mixed `is_done=True/False`

### Problem: Admin login fails

- Confirm superuser exists:

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
U = get_user_model()
print(U.objects.filter(is_superuser=True).values_list("username", flat=True))
```

### Problem: Port already in use

Run on another port:

```bash
python manage.py runserver 8001
```

## 12. Current Limitations

- Only `GET` list endpoints are implemented
- No create/update/delete API yet
- No pagination/filtering for API
- No test coverage yet

## 13. Suggested Next Improvements

- Add `POST /api/todos/`
- Add detail endpoint: `GET /api/todos/<id>/`
- Add update/delete support
- Add test cases in `api/tests.py`
- Add API docs tooling (Swagger/OpenAPI)

## 14. Additional Learning Notes

See detailed learning journal:

- `DAY1_LEARNING.md`
