
from django.urls import path 
from home.views import *



urlpatterns = [
    
    path("",index,name="index"),
    path('get_project_data/<int:project_id>/', get_project_data, name='get_project_data'),
    path('update?', update_task, name='update_task'),
    path('update_status/<int:task_id>/<str:status>/', update_status, name='update_status'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('add/', add_task, name='add_task'),
    path('add_project/', add_project, name='add_project'),
    path("register/" , register ,name ="register"),
    path("login/" , user_login ,name ="login"),
    path('logout/', user_logout, name='logout'),
 
    ]
