from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home),  # Include the blog app's URLs
    path('about/', views.about),  # Example of another view
]
