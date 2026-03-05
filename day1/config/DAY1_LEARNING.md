# Day 1 Learning Documentation (Django REST Framework)

Date: 2026-03-03
Project Path: `day1/config`

## 1. What I Built Today
- Created a basic Django + DRF Todo API project.
- Added one app: `api`.
- Created `Todo` model.
- Built serializer and API view for listing todos.
- Connected endpoint: `/api/todos/`.
- Enabled Django admin with `TodoAdmin`.
- Prepared superuser login flow and added sample todo data.

## 2. Project Structure (Important Files)
- `day1/config/manage.py`
- `day1/config/config/settings.py`
- `day1/config/config/urls.py`
- `day1/config/api/models.py`
- `day1/config/api/serializers.py`
- `day1/config/api/views.py`
- `day1/config/api/urls.py`
- `day1/config/api/admin.py`

## 3. Setup Steps Practiced
```bash
cd "e:\Md-Rabbi-Islam\DJANGO-REST-FRAMEWORK\day1\config"
python -m venv Env
.\Env\Scripts\activate
pip install django djangorestframework
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 4. Core Code Implemented

### Model (`api/models.py`)
```python
class Todo(models.Model):
    title = models.CharField(max_length=120)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Serializer (`api/serializers.py`)
```python
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
```

### API View (`api/views.py`)
```python
@api_view(['GET'])
def todo_list(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)
```

### App URLs (`api/urls.py`)
```python
urlpatterns = [
    path('todos/', todo_list),
]
```

### Project URLs (`config/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

## 5. Admin Panel Enable
`api/admin.py`:
```python
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_done", "created_at")
    list_filter = ("is_done",)
    search_fields = ("title",)
```

Admin URL:
- `http://127.0.0.1:8000/admin/`

## 6. API Endpoints Tested
- Pending todo list:
  - `GET http://127.0.0.1:8000/api/todos/`
- Completed todo list:
  - `GET http://127.0.0.1:8000/api/done-todos/`

Sample response:
```json
[
  {"id": 2, "title": "Build Todo API endpoint", "is_done": false, "created_at": "..."},
  {"id": 1, "title": "Learn DRF serializers", "is_done": false, "created_at": "..."}
]
```
Done endpoint sample:
```json
[
  {"id": 3, "title": "Test admin panel login", "is_done": true, "created_at": "..."}
]
```

## 7. Data Added Today
Created 3 todos:
- `Learn DRF serializers` -> `is_done=False`
- `Build Todo API endpoint` -> `is_done=False`
- `Test admin panel login` -> `is_done=True`

## 8. Common Problems Faced and Fixes

### Problem 1: `/api/todos/` returned 404
Reason:
- Wrong Django project/server was running on port `8000`.

Fix:
- Run server from correct folder:
```bash
cd "e:\Md-Rabbi-Islam\DJANGO-REST-FRAMEWORK\day1\config"
python manage.py runserver 127.0.0.1:8001
```
- Then open:
  - `http://127.0.0.1:8001/api/todos/`

### Problem 2: Admin login failed
Reason:
- Password mismatch or wrong running DB.

Fix:
- Reset admin user and password in current project DB:
```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); u=U.objects.get(username='admin'); u.is_staff=True; u.is_superuser=True; u.set_password('Admin@12345'); u.save()"
```

## 9. Git Learning (Contributor Issue)
What happened:
- A commit used wrong author/email, so GitHub showed extra contributor.

Fix learned:
- Set correct identity:
```bash
git config --global user.name "RabbiPrimon"
git config --global user.email "rabbiprimon00000@gmail.com"
```
- Amend last commit author and force push:
```bash
git commit --amend --author="RabbiPrimon <rabbiprimon00000@gmail.com>" --no-edit
git push --force-with-lease origin main
```

## 10. Key Concepts Learned Today
- DRF `ModelSerializer`
- Function-based API with `@api_view`
- URL routing (`project urls` + `app urls`)
- Queryset filtering by status (`is_done=True/False`)
- Django admin model registration and customization
- Superuser/staff authentication basics
- Debugging 404 due to wrong server/project
- Git author identity and contributor history behavior

## 11. Next Day Plan
- Add `POST /api/todos/` for create todo.
- Add detail endpoint: `GET /api/todos/<id>/`.
- Add update/delete methods.
- Add pagination and ordering.
- Add `.gitignore` and remove `Env/` from repository tracking.
