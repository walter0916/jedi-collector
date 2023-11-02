from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('jedi/create', views.JediCreate.as_view(), name='jedi-create'),
  path('jedi/', views.jedi_index, name='jedi-index'),
  path('jedi/<int:jedi_id>/', views.jedi_detail, name="jedi-detail")
]