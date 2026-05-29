from django.urls import path
from . import views

app_name = 'wordcounter'

urlpatterns = [
    path('', views.index, name='home'),
]