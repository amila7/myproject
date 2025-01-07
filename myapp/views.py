from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from  .models import Feature
# Create your views here.
def index(request):
    features = Feature.objects.all()
    return render(request, 'index.html', {'features': features})


def counter(request):
    text = request.POST['text']
    amount_of_words = len(text.split())
    return render(request, 'counter.html', {'amount_words': amount_of_words})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not email or not password or not password2:
            messages.error(request, 'All fields are required.')
            return redirect('register')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already used.')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already used.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
    else:
        return render(request, 'register.html')