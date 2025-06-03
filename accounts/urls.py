from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.login_view, name = 'login'),
    path('signup/',views.student_view, name = 'signup'),
    path('student/',views.student_view, name = 'student'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.change_password_view, name = 'change_password'),
]