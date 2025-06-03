from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_payment, name='submit_payment'),
    path('status/', views.payment_status, name='payment_status'),
]
