from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import userlogin, Password_change_form, GenderSelectionForm
from django.contrib import messages 
from django.contrib.auth.models import User



def login_view(request):
    form = userlogin(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username').lower()
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('student')
            else:
                if not User.objects.filter(username=email).exists():
                    new_user = User.objects.create_user(username=email, password=password)
                    login(request, new_user)
                    return redirect('student')
                else:
                    messages.error(request, "Invalid password for existing account!")

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def student_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = GenderSelectionForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Gender updated successfully.")
            return redirect('student')
    else:
        form = GenderSelectionForm(instance=profile)

    booking = {
        'hostel_name': 'Hall 3',
        'room_number': 'B12',
        'check_in_date': '2025-05-01',
        'check_out_date': '2025-12-15',
    }

    context = {
        'user': request.user,
        'booking': booking,
        'current_year': timezone.now().year,
        'form': form, 
        'gender': profile.gender or "Not selected",
    }

    return render(request, 'accounts/student.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = Password_change_form(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Prevents logout
            messages.success(request, 'Password successfully changed.')
            return redirect('student')  # Redirect to your dashboard or home
    else:
        form = Password_change_form(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})