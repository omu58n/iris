from django.urls import path
from . import views

urlpatterns = [
    path('', views.input, name='input'),
    path('figure', views.figure, name='figure'),
    path('output/<int:pk>/', views.output, name='output')
]
