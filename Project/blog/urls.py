from django.urls import path,include
from . import views

app_name = 'blog' 

urlpatterns = [
    path('', views.posts,name='post'),  
    path('<int:id>/', views.post_detail, name='post_detail'),  

]
