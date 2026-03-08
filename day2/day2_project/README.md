# Day 2 Django REST Todo API

A simple Todo API built with Django and Django REST Framework (DRF).

## 1. Project Summary

This project provides basic Todo management endpoints:
- List pending todos
- Create a new todo
- List completed todos

It also includes:
- Django admin configuration for the `Todo` model
- API test coverage with `APITestCase`

## 2. Tech Stack

- Python: `3.12.6`
- Django: `5.1.1`
- Django REST Framework: `3.16.1`
- Database: SQLite (`db.sqlite3`)

## 3. Current Data Model

Model: `Todo`

Fields:
- `id` (auto-generated, primary key)
- `title` (`CharField`, max length `120`)
- `is_done` (`BooleanField`, default `False`)
- `created_at` (`DateTimeField`, auto set on create)

Source: `day2_app/models.py`

## 4. API Endpoints

Base URL: `http://127.0.0.1:8000/`

### 4.1 Get pending todos

- Method: `GET`
- URL: `/todos/`
- Behavior: returns only `is_done=False` todos, ordered by newest first.

Example response:
```json
[
  {
    "id": 1,
    "title": "Learn DRF",
    "is_done": false,
    "created_at": "2026-03-08T08:10:00Z"
  }
]
```

### 4.2 Create todo

- Method: `POST`
- URL: `/todos/create/`
- Body (JSON):

```json
{
  "title": "Write tests",
  "is_done": false
}
```

- Success: `201 Created`
- Validation error: `400 Bad Request`

### 4.3 Get completed todos

- Method: `GET`
- URL: `/done-todos/`
- Behavior: returns only `is_done=True` todos, ordered by newest first.

## 5. URL Routing

- Project-level routes: `day2_project/urls.py`
- App-level routes: `day2_app/urls.py`

Routing flow:
1. `day2_project/urls.py` includes `day2_app.urls`
2. `day2_app/urls.py` maps each endpoint to view functions in `day2_app/views.py`

## 6. Serializer Layer

`TodoSerializer` uses:
```python
fields = "__all__"
```

So all model fields are automatically exposed in API responses and accepted in requests (subject to Django model validation).

Source: `day2_app/serializers.py`

## 7. Admin Panel

Admin registration is configured in `day2_app/admin.py`:
- `list_display`: `id`, `title`, `is_done`, `created_at`
- `list_filter`: `is_done`
- `search_fields`: `title`

Admin URL:
- `http://127.0.0.1:8000/admin/`

## 8. Setup and Run

From `day2/day2_project`:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

## 9. Testing

Test file: `day2_app/tests.py`

Covered test cases:
- Create todo (`POST /todos/create/`)
- Pending list (`GET /todos/`)
- Done list (`GET /done-todos/`)

Run tests:
```powershell
python manage.py test
```

## 10. Migrations

Current migrations:
- `0001_initial.py`
- `0002_remove_todo_description_remove_todo_updated_at_and_more.py`

Important: `0002` removes `description` and `updated_at`, and changes `title` length to `120`.

If you change model fields, always run:
```powershell
python manage.py makemigrations
python manage.py migrate
```

## 11. Troubleshooting

### 11.1 `OperationalError: no such column ...`

Cause:
- Model code and database schema are out of sync.
- Or an old `runserver` process is still running stale code.

Fix:
```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*manage.py*runserver*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
python manage.py migrate
python manage.py check
python manage.py runserver
```

### 11.2 Serializer/model mismatch

If serializer expects fields not present in model:
1. Update serializer to match model
2. Create and apply migrations if model changed
3. Re-run tests

## 12. Development Workflow (Recommended)

1. Change model/view/serializer
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Run `python manage.py test`
5. Run `python manage.py runserver`

## 13. Project Structure

```text
day2_project/
├─ manage.py
├─ db.sqlite3
├─ day2_project/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
└─ day2_app/
   ├─ admin.py
   ├─ apps.py
   ├─ models.py
   ├─ serializers.py
   ├─ tests.py
   ├─ urls.py
   ├─ views.py
   └─ migrations/
      ├─ 0001_initial.py
      └─ 0002_remove_todo_description_remove_todo_updated_at_and_more.py
```

