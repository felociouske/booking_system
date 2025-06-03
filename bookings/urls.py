from django.urls import path
from .import views

urlpatterns = [
    path('book/', views.book_room, name='book_room'),
    path('success/', views.booking_success, name='booking_success'),
]