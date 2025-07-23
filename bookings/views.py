from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Booking, Room
from payment.models import Payment
from .forms import RoomBookingForm
from django.db.models import Sum



@login_required
def book_room(request):
    user = request.user

    # Check for existing booking (don't redirect)
    existing_booking = Booking.objects.filter(user=user).first()
    already_booked = existing_booking is not None

    # Sum total approved payments
    total_paid = Payment.objects.filter(user=user, status='approved').aggregate(Sum('amount'))['amount__sum'] or 0
    eligible = total_paid >= 6500

    if not eligible:
        remaining = 6500 - total_paid
        messages.warning(
            request, 
            f"You have paid KES {total_paid}. You need KES {remaining} more to book a room."
        )
        return redirect('submit_payment')

    # Show rooms matching gender
    gender = user.profile.gender
    available_rooms = Room.objects.filter(gender=gender)

    if request.method == 'POST' and not already_booked and eligible:
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
        'total_paid': total_paid,
        'eligible': eligible,
        'already_booked': already_booked,
        'booking': existing_booking,
    })

@login_required
def booking_success(request):
    # Get the booking for the logged-in user
    booking = Booking.objects.get(user=request.user)

    # Render the booking info page
    return render(request, 'bookings/booked_rooms.html', {'booking': booking})
