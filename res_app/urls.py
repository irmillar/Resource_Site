from django.urls import path
from . import views

# Allow template tagging for URLs by including the 'app_name' variable
app_name = 'res_app'

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('new/', views.new_res, name='new_res'),
    path('register/', views.register, name='register'),
    path('details/<int:pk>/', views.res_details, name='res_details'),
    path('details/<int:pk>/edit', views.res_edit, name='res_edit'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),
]
