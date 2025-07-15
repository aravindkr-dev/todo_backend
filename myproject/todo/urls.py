from django.urls import path
from .views import hello_world , get_task , register , login , get_session , logout , create_task , delete_task , change_status , view_users

urlpatterns = [
    path('hello/' , hello_world),
    path('tasks/' , get_task),
    path('register/' , register),
    path('login/' , login),
    path('session/' , get_session),
    path('logout/' , logout),
    path('add_task/' , create_task),
    path('del_task/<int:pk>/' , delete_task),
    path('change_status/<int:pk>' , change_status),
    path('view_users/' , view_users)
]