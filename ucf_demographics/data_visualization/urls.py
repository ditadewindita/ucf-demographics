from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:college>/<str:term>/', views.college_data, name='college_data'),
]
