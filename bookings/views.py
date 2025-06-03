from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Booking, Room
from payment.models import Payment
from .forms import RoomBookingForm

@login_required
def book_room(request):
    user = request.user

    # Check if already booked
    existing_booking = Booking.objects.filter(user=user).first()
    if existing_booking:
        messages.info(request, "You have already booked a room.")
        return redirect('booking_success')

    # Payment check (unchanged)
    try:
        payment = Payment.objects.get(user=user)
        if payment.status != 'approved':
            messages.warning(request, "Your payment is still pending approval by admin.")
            return redirect('submit_payment')
    except Payment.DoesNotExist:
        messages.warning(request, "Please submit your M-Pesa payment first.")
        return redirect('submit_payment')

    # Show rooms matching gender
    gender = user.profile.gender
    available_rooms = Room.objects.filter(gender=gender)

    if request.method == 'POST':
        form = RoomBookingForm(request.POST, user=user)
        if form.is_valid():
            room = form.cleaned_data['room']
            side = form.cleaned_data.get('hall6_side')

            booking = Booking(
                user=user,
                room=room,
                hall6_side=side if room.hall == "Hall 6" else None
            )
            booking.save()

            messages.success(request, "Room booked successfully!")
            return redirect('booking_success')
    else:
        form = RoomBookingForm(user=user)

    return render(request, 'bookings/book_room.html', {
        'form': form,
        'rooms': available_rooms,
    })



@login_required
def booking_success(request):
    # Get the booking for the logged-in user
    booking = Booking.objects.get(user=request.user)

    # Render the booking info page
    return render(request, 'bookings/booked_rooms.html', {'booking': booking})
