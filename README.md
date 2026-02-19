# Django REST-API

<details>
<summary>Start with REST API</summary>

## What is Serializer?
Serializer allow complex data such as querysets and model instances to be converted to natvie python datatypes that can then be easily rendered into JSON, XML or other content types.

## API Create
+ Create and Activate Environment
    ```text
    python-m venv env

    .\env\Scripts\activate
    ```
+ Install requirted packages:
    ```python
    pip install django
    pip install djangorestframework
    ```
+ Set up a new Django application.
    ```python
    django-admin startproject restApiProject  
    cd restApiProject
    django-admin startapp restApiApp
    ```
+ Update `settings.py` to Add `rest_framework` and `app name` to INSTALLED_APPS:
    ```python
    INSTALLED_APPS = [
    ......
    ......
    'rest_framework',
    'restApiApp',
    ]
    ```
+ Create models into `models.py` script:
    ```python
    class ModelName(models.Model):
        teacher_name = models.CharField(max_length=30, null=True)
        course_name = models.CharField(max_length=50, null =True)
        course_duration = models.IntegerField(null=True)
        seat = models.IntegerField(null=True)

    ```
+ Regsiter model into the `admin.py`:
    ```python
    @admin.register(ApiModel)
    class ApiModelAdmin(admin.ModelAdmin):
        list_display=['id','teacher_name','course_name','course_duration','seat']
    ```
+ Include the urls into the `urls.py`
    ```python
    from django.urls import path, include
    urlpatterns = [
        .......
        .......
        path('api-auth/', include('rest_framework.urls')),
    ]
    ```
+ After that create a serializer script file under the app like: `serializer.py`:
    ```python
    from rest_framework import serializers

    class ApiModelSerializer(serializers.Serializer):
        teacher_name = serializers.CharField(max_length=30)
        course_name = serializers.CharField(max_length=50)
        course_duration = serializers.IntegerField()
        seat = serializers.IntegerField()
    ```
### Access All data from model:
+ At first, create a view function:
    ```python
    from django.shortcuts import render, HttpResponse
    from .models import *
    from .serializers import *
    from rest_framework.renderers import JSONRenderer
    #----Qyeryset--------
    def apimodel_info(request):
        #---complex data
        apidata = ApiModel.objects.all()
        #---python dict
        serializer = ApiModelSerializer(apidata, many=True)
        #---render Json
        json_data = JSONRenderer().render(serializer.data)
        #----Json sent to user
        return HttpResponse(json_data, content_type='application/json')
    ```
    + `ApiModelSerializer(apidata, many=True)` creates a serializer instance that converts the queryset `apidata` into a Python data structure (like a list of dictionaries). The `many=True` argument indicates that multiple objects are being serialized.
    + `JSONRenderer().render(serializer.data)` converts the serialized data (a Python dict) into a JSON-formatted string. The result is stored in `json_data`.
    + `HttpResponse(json_data, content_type='application/json')` creates an HTTP response with the JSON data and specifies that the content type is `'application/json'`. This response is returned to the client (user).
+ Include Urls:
    ```python
    ..........
    ..........
    path('apiinfo/',views.apimodel_info),
    ..........
    ```
+ Then run the project. After run the project we can view all data as json format.

### View single instance:
+ At first, create a view function:
    ```python
    def apimodel_instance(request,pk):
        #---complex data
        apidata = ApiModel.objects.get(id=pk)
        #---python dict
        serializer = ApiModelSerializer(apidata)
        #---render Json
        json_data = JSONRenderer().render(serializer.data)
        #----Json sent to user
        return HttpResponse(json_data, content_type='application/json')
    ```
### Access data from third pary app:
```python
import requests

#---allocate url

URL = "http://127.0.0.1:8000/apiinfo/"

#-----get url data
response = requests.get(url=URL)
#---extract into json
data = response.json()
print(data)
```


## What is DeSerializer?
- The process of converting native python datatypes such as dictionaries to complex data types such as querysets is called deserializer in DRF.
- Serializers also provide deserialization, allowing parsed data to be convertd back into complex types, after first validating the incoming data.

### Insert/Create data into model from third party app:
+ Create a function under the serializer class into `serializer.py` script:
    ```python
    class ApiModelSerializer(serializers.Serializer):
        ...........
        ...........
        def create(self, validated_data):
            return ApiModel.objects.create(**validated_data)
    ```
+ Create a view function into the `views.py`:
    ```python
    from django.views.decorators.csrf import csrf_exempt
    import io
    from rest_framework.parsers import JSONParser
    @csrf_exempt
    def apidata_create(request):
        if request.method == 'POST':
            json_data = request.body
            #json to stream convert
            stream = io.BytesIO(json_data)
            #stream to python
            pythondata = JSONParser().parse(stream)
            #python to complex
            serializer = ApiModelSerializer(data=pythondata)
            if serializer.is_valid():
                serializer.save()
                res = {'msg':'Successfully insert data'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type ='application.json')
    ```
+ Create urls:
    ```python
    ..............
    ..............
    path('apicreate/',views.apidata_create, name='apicreate'),
    ..............
    ```
+ Create a python script `create.py` outside the project like a third party app insert the data:
    ```python
    import requests, json

    URL = "http://127.0.0.1:8000/apicreate/"

    data = {
        'teacher_name': 'Rohim',
        'course_name': 'Deep Learning',
        'course_duration': 3,
        'seat': 20,
    }

    json_data = json.dumps(data)
    re = requests.post(url=URL, data = json_data)
    data = re.json()
    print(data)
    ```

### Update model data from third party app:
+ Create a function under the serializer class into `serializer.py` script:
    ```python
    class ApiModelSerializer(serializers.Serializer):
        ...........
        ...........
        def update(self, instance, validated_data):
            instance.teacher_name = validated_data.get('teacher_name', instance.teacher_name)
            instance.course_name = validated_data.get('course_name', instance.course_name)
            instance.course_duration = validated_data.get('course_duration', instance.course_duration)
            instance.seat = validated_data.get('seat', instance.seat)
            
            instance.save()
            return instance
    ```
+ Create a view function into the `views.py` without create new function we can include `PUT` method code under the `POST` method function:
    ```python
    from django.views.decorators.csrf import csrf_exempt
    import io
    from rest_framework.parsers import JSONParser
    @csrf_exempt
    def apidata_update(request):    
        if request.method == 'PUT':
            json_data = request.body
            #---json to stream
            stream = io.BytesIO(json_data)
            #stream to python
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('id')
            apidata = ApiModel.objects.get(id=id)
            serializer = ApiModelSerializer(apidata, data=pythondata, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {'msg':'Successfully update data'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type ='application.json')
    ```
+ Create urls:
    ```python
    ..............
    ..............
    path('apiupdate/',views.apidata_update, name='apiupdate'),
    ..............
    ```
+ Create a python script `update.py` outside the project like a third party app insert the data:
    ```python
    import requests
    import json

    URL = "http://127.0.0.1:8000/apiupdate/"

    data = {
        'id': 2,
        'teacher_name': 'Md. Abul',
        'course_name': 'Web Development',
    }

    json_data = json.dumps(data)
    r = requests.put(url=URL, data=json_data)
    data = r.json()
    print(data)
    ```

### Delete model data from third party app:
+ Create a function into the `views.py` without create new function we can include `DELETE` method code under the `POST/PUT` method function:
    ```python
    from django.views.decorators.csrf import csrf_exempt
    import io
    from rest_framework.parsers import JSONParser
    @csrf_exempt
    def apidata_delete(request):    
        if request.method == 'DELETE':
            json_data = request.body
            print(json_data)
            #--json to stream
            stream = io.BytesIO(json_data)
            #--stream to python
            pythondata = JSONParser().parse(stream)
            id = pythondata.get('id')
            if ApiModel.objects.filter(id=id).exists():
                apidata = ApiModel.objects.get(id=id)
                apidata.delete()
                res = {'msg':'Successfully deleted data'}
            else:
                res = {'msg':'Data not found'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application.json')
    ```
+ Create urls:
    ```python
    ..............
    ..............
    path('apidelete/',views.apidata_delete, name='apidelete'),
    ..............
    ```
+ Create a python script `delete.py` outside the project like a third party app insert the data:
    ```python
    import requests
    import json

    URL = "http://127.0.0.1:8000/apidelete/"

    data = {
        'id' : 5,
    }
    #-----Convert python data into json
    json_data = json.dumps(data)
    r = requests.delete(url=URL, data = json_data)
    #-----extract
    data = r.json()
    print(data)
    ```

</details>

<details>
<summary>Rest API follow by documentation</summary>

## Start With API
+ Create and Activate Environment
    ```text
    python-m venv env

    .\env\Scripts\activate
    ```
+ Install requirted packages:
    ```python
    pip install django
    pip install djangorestframework
    ```
+ Set up a new Django application.
    ```python
    django-admin startproject restApiProject  
    cd restApiProject
    django-admin startapp restApiApp
    ```
+ Update `settings.py` to Add `rest_framework` and `app name` to INSTALLED_APPS:
    ```python
    INSTALLED_APPS = [
    ......
    ......
    'restApiApp',
    'rest_framework',
    ]
    ```
+ Create a model into the `models.py` files:
    ```python
    class studentModel(models.Model):
        name = models.CharField(max_length=100,null=True)
        email = models.EmailField(max_length=100,null=True)
        address = models.CharField(max_length=100,null=True)
        
        def __str__(self):
            return self.name
    ```
+ Register the model into `admin.py`:
    ```python
    from restApiApp.models import studentModel

    admin.site.register(studentModel)
    ```
+ Create a new module named `serializers.py` and create a model `serializer class` under the `restApiApp` that we'll use for our data representations.:
    ```python
    from rest_framework import serializers
    from restApiApp.models import studentModel

    class studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = studentModel
        fields = ['id','name','address','email']
    ```

## Inspact Serializer Data:
If we want we can inspect all the fields in a serializer instance.
+ Open django shell into the terminal:
    ```python
    py manage.py shell
    ```
+ Then try the following command:
    + First import `StudentSerializer` from `serializers.py`:
        ```python
        from restApiApp.serializers import StudentSerializer
        ```
    + Create a object variable:
        ```python
        serializer = StudentSerializer()
        print(repr(serializer))
        ```

## Work with Django Shell:

+ Open django shell into the terminal:
    ```python
    py manage.py shell
    ```
+ Now create object:
    + import `studentModel` from model:
        ```python
        from restApiApp.models import studentModel
        ```
    + create objects:
        ```python
        obj = studentModel()
        ```
    + assign the value into the object:
        ```python
        obj.name="Md Shakil"
        obj.address="Dhaka"
        obj.email="shakil.eub.cse@gmail.com"
        ```
    + save the object:
        ```python
        obj.save()   
        ```
    + delete object:
        ```python
        obj.delete()
        ```

## Django views using Serializer class into Web:

### View API data using `JsonResponse`:
+ Edit `views.py` and import required packages:
    ```python
    from django.shortcuts import render
    from django.http import HttpResponse, JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from rest_framework.parsers import JSONParser
    ```
+ Import `serializers` and `models` from `restApiApp`:
    ```python
    from restApiApp.serializers import StudentSerializer
    from restApiApp.models import studentModel
    ```
+ Create data view function:
    ```python
    @csrf_exempt
    def student_list(request):
        if request.method == 'GET':
            objs = studentModel.objects.all()
            serializer = studentModelSerialize(objs, many=True)
            return JsonResponse(serializer.data, safe=False)
    ```

+ Create url into the `urls.py`:

    ```python
    from django.contrib import admin
    from django.urls import path
    from RestApiApp2.views import student_list
    from RestApiApp2.apiviews import studentModel

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('list/',student_list),
    ]
    ```
        
    + Import `student_list` function from `views.py` and import `studentModel` from `models.py`.

+ Create another data view function for view the individual data using primary key:
    ```python
    @csrf_exempt
    def student_detail(request, pk):
        try:
            student = studentModel.objects.get(pk=pk)
        except studentModel.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = studentModelSerialize(student)
            return JsonResponse(serializer.data)
    ```
+ Create url into the `urls.py`:
    ```python
    ...............
    ...............
    from RestApiApp2.views import student_detail

    urlpatterns = [
        .............
        .............
        path('student_detail/<int:pk>/',student_detail),
    ]
    ```

</details>
