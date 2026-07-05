from django.urls import path ,include
from . import views 

urlpatterns = [
    # The empty string '' means this is the root of the gallery app
    path('index/', views.index),
]
