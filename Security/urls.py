from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('start/', views.start, name = 'start'),
    path('about/', views.about, name = 'about'),
    path('data/', views.output, name = 'output')
]
 