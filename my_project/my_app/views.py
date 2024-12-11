from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.utils.timezone import localtime, now
from datetime import time

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            current_time = localtime(now()).time()
            
            if user.is_superuser or user.role == 'admin':
                login(request, user)
                return redirect('/admin/')  # Admin dashboard
           
           
            time_range = user.allowed_time_ranges
            start_time = time.fromisoformat(time_range.get('start'))
            end_time = time.fromisoformat(time_range.get('end'))

            if start_time <= current_time <= end_time:
                login(request, user)
                return redirect('/')  # Redirect to user dashboard
            else:
                return HttpResponse("Login restricted to allowed time ranges.", status=401)
        else:
            context = {"error": "Invalid credentials. Please try again."}
            return render(request, 'my_app/login.html', context)
    return render(request, 'my_app/login.html')
