from django.urls import path
from .views import todo_list, done_todo_list, create_todo

urlpatterns = [
    path('todos/', todo_list, name='todo-list'),
    path('todos/create/', create_todo, name='create-todo'),
    path('done-todos/', done_todo_list, name='done-todo-list'),
]