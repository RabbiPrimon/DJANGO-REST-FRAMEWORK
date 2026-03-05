from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer

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
