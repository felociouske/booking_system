from django.contrib import admin
from .models import Room,Booking

@admin.register(Room)
class RoomAdmin (admin.ModelAdmin):
    list_display = ('hall', 'room_number','gender', 'capacity')
    list_filter = ('hall', 'gender')
    search_fields = ('hall', 'room_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'hall6_side', 'date_booked')
    list_filter = ('room__hall', 'hall6_side')
    search_fields = ('user_username', 'room__room_number')

