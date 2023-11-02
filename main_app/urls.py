from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('jedi/create', views.JediCreate.as_view(), name='jedi-create'),
]