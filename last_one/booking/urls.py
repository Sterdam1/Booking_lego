from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('singin/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_event/', views.create_event, name='create_event'),
    path('create_event_conformation/', views.create_event_conformation, name='create_event_conformation'),
    path('services/', views.choose_service, name='choose_service'),
    path('table/<str:table_name>/', views.table_view, name='table_view'), 
]