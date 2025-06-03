from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    HALL_CHOICES = (
        ('Hall 1', 'Hall 1'),
        ('Hall 2', 'Hall 2'),
        ('Hall 3', 'Hall 3'),
        ('Hall 4', 'Hall 4'),
        ('Hall 5', 'Hall 5'),
        ('Hall 6', 'Hall 6'),
    )

    hall = models.CharField(max_length=20, choices=HALL_CHOICES)
    room_number = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.hall} - Room {self.room_number} ({self.gender})"
    @property
    def current_occupants(self):
        if self.hall == 'Hall 6':
            # Each side has 2 beds, check both sides
            side_a = Booking.objects.filter(room=self, hall6_side='A').count()
            side_b = Booking.objects.filter(room=self, hall6_side='B').count()
            return {'A': side_a, 'B': side_b}
        else:
            return Booking.objects.filter(room=self).count()
    
    def save(self, *args, **kwargs):
        if self.hall != 'Hall 6':
            self.capacity = 4
        super().save(*args, **kwargs)

class Booking(models.Model):
    HALL6_SIDES = (
        ('A', 'Side A'),
        ('B', 'Side B'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hall6_side = models.CharField(max_length=1, choices=HALL6_SIDES, null=True, blank=True)
    date_booked = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.room.hall == 'Hall 6':
            return f"{self.user.username} - {self.room} (Side {self.hall6_side})"
        return f"{self.user.username} - {self.room}"



