from django.shortcuts import render, redirect
from .forms import PaymentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Payment, PaymentInfo
from django.db.models import Sum


@login_required
def submit_payment(request):
    payment_info = PaymentInfo.objects.first()
    if not payment_info:
        payment_info = PaymentInfo.objects.create()  # Create default if none exists


    # Total approved payments
    total_paid = Payment.objects.filter(user=request.user, status='approved').aggregate(Sum('amount'))['amount__sum'] or 0

    if total_paid >= 6500:
        messages.success(request, f"You have already paid KES {total_paid}. You can now book a room.")
        return redirect('book_room')
    # Handle form submission
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.status = 'pending'  # Set status manually
            payment.save()
            messages.success(request, "Payment submitted! Please wait for admin approval.")
            return redirect('payment_status')  # redirect after successful submission
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'payment_info': payment_info,
    }
    return render(request, 'payment/submit_payment.html', context)

@login_required
def payment_status(request):
    payment = Payment.objects.filter(user=request.user).first()
    if payment and payment.status == 'approved':
        return redirect('book_room')  # Redirect to room booking page
    return render(request, 'payment/payment_status.html', {'payment': payment})
