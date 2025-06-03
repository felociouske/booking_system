from django.shortcuts import render, redirect
from .forms import PaymentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Payment, PaymentInfo

@login_required
def submit_payment(request):
    payment_info = PaymentInfo.objects.first()
    if not payment_info:
        payment_info = PaymentInfo.objects.create()  # Create default if none exists

    # Check if user has a payment already
    if hasattr(request.user, 'payment'):
        if request.user.payment.status == 'approved':
            messages.success(request, "Payment already approved. You can now book a room.")
            return redirect('book_room')
        else:
            messages.info(request, "Your payment is under review.")
            return redirect('payment_status')

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
