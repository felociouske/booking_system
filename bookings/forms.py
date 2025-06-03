from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, Room

class RoomBookingForm(forms.Form):
    room_choice = forms.CharField(label="Choose Room")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_room_choice(self):
        value = self.cleaned_data['room_choice']

        try:
            if "|" in value:
                room_id_str, side = value.split("|")
                room_id = int(room_id_str)
                side = side.upper()
                if side not in ['A', 'B']:
                    raise ValidationError("Invalid side selection. Use A or B.")
            else:
                room_id = int(value)
                side = None
        except ValueError:
            raise ValidationError("Invalid room selection format. Example: '2262|A' or '45'.")

        # Ensure room exists
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise ValidationError("Selected room does not exist.")

        # Gender-based restriction
        if self.user and self.user.profile.gender != room.gender:
            raise ValidationError("You cannot book a room for the opposite gender.")

        # Room capacity checks
        existing_bookings = Booking.objects.filter(room=room)
        if room.hall == "Hall 6":
            if not side:
                raise ValidationError("Please select Hall 6 side: A or B.")
            side_count = existing_bookings.filter(hall6_side=side).count()
            if side_count >= 2:
                raise ValidationError(f"Side {side} of Room {room.room_number} is already full.")
        else:
            if existing_bookings.count() >= room.capacity:
                raise ValidationError("This room is already full.")

        # Store parsed values
        self.cleaned_data['room'] = room
        self.cleaned_data['hall6_side'] = side

        return value
