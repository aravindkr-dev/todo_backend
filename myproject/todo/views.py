from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users , Task
from .serializer import UserSerializer , TaskSerializer
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth import authenticate

#Get all the tasks
@api_view(['GET'])
def hello_world(request):
    return Response({"message" : "Hello World"})

#Create tasks
@api_view(['POST'])
def create_task(request):
    username , logged_in = request.session.get('username' , None) , request.session.get('is_logged_in' , None)
    if username and logged_in:
        task = request.data.get('task')
        data = {
            "task" : task,
            "user_name" : username
        }
        serial = TaskSerializer(data = data)
        try:
            if serial.is_valid():
                serial.save()
                tasks = Task.objects.filter(user_name=username)
                serializer = TaskSerializer(tasks, many=True)
                if tasks.exists():
                    return Response(serializer.data, status=201)
        except Exception as e:
            return Response({"message" : "Couldn't ass task" , "error" : str(e)} , status = 400)




#View all tasks
@api_view(['GET'])
def get_task(request):
    user_name = request.session.get("username" , None)
    logged_in = request.session.get("is_logged_in" , None)
    if user_name and logged_in:
        tasks = Task.objects.filter(user_name = user_name)
        serializer = TaskSerializer(tasks , many=True)
        if tasks.exists():
            return Response(serializer.data ,status=201)
        return Response({"message" : "No tasks found"} , status=200)
    else:
        return Response({"message": "Login to create task"}, status=404)



#Delete task

@api_view(["DELETE"])
def delete_task(request , pk):
    try:
        task = Task.objects.get(id = pk)
        task.delete()
        return Response({"message" : "task deleted successfully"} , status=201)
    except Task.DoesNotExist:
        return Response({"message" : "task not found"} , status=404)



#Status
@api_view(["PUT"])
def change_status(request , pk):
    try:
        task = Task.objects.get(id = pk)
        task.status = True if task.status == False else False
        task.save()
        return Response({"message" : "Status changed successfully"} , status=201)

    except Task.DoesNotExist:
        return Response({"message" : "task not found"} , status=404)


#Registration
@api_view(['POST'])
def register(request):
    user_name = request.data.get("user_name")
    password = request.data.get("password")

    if not user_name or not password:
        return Response({"message" : "Username and Password fields ar required"})

    try:
        data = {
            "user_name" : user_name,
            "password" : make_password(password)
        }
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "User registration Successful" } , status = 201)
    except Exception as e:
        return Response({"message" : "Registration Failed" , "error" : str(e)} , status = 400)


#Login
"""
@api_view(["POST"])
def login(request):
    user_name = request.data.get("user_name")
    password = request.data.get("password")
    user = Users.objects.get(user_name = user_name)

    if user and check_password(password , user.password):
        request.session['username'] = user_name
        request.session['is_logged_in'] = True
        return Response({"message" : "true"} , status = 201)
    return Response({"message" : "false"} , status = 401)
"""


@api_view(["POST"])
def login(request):
    user_name = request.data.get("user_name")
    password = request.data.get("password")

    try:
        user = Users.objects.get(user_name=user_name)
    except Users.DoesNotExist:
        return Response({"message": "User does not exist"}, status=404)

    if check_password(password, user.password):
        request.session['username'] = user_name
        request.session['is_logged_in'] = True
        return Response({"message": "User login successful"}, status=201)

    return Response({"message": "Wrong login credentials"},status = 401)

#check session
@api_view(["GET"])
def get_session(request):
    username = request.session.get('username', None)
    logged_in = request.session.get('is_logged_in' , None)
    if username and logged_in:
        return Response({'username': username , "is_logged_in" : logged_in})
    else:
        return Response({'message': "You are logged out"  ,"is_logged_in" : logged_in})


#Logout
@api_view(['GET'])
def logout(request):
    request.session.flush()
    return Response({"message" : "User logged out successfully"})

#View Users

@api_view(["GET"])
def view_users(request):
    user = Users.objects.all()
    serializer = UserSerializer(user , many=True)
    try:
        if user.exists():
            return Response({"message" : f"User found -  {serializer.data}"})
    except Exception as e:
        return Response({"message" : "operation failed" , "error" : str(e)})