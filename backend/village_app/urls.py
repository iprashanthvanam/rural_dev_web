
# backend\village_app\urls.py

from django.urls import path
from . import views

# backend\village_app\urls.py
urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('success/<int:village_id>/', views.success, name='success'),
]