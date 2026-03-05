from django.urls import path
from .views import todo_list, done_todo_list

urlpatterns = [
    path('todos/', todo_list),
    path('done-todos/', done_todo_list),
]
