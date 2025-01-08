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
    posts = [1,2,3,4,5,'tim','tom','john']

    # text = request.POST['text']
    # amount_of_words = len(text.split())
    return render(request, 'counter.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username'] 
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

        except KeyError as e:
            messages.error(request, f'Missing required field: {str(e)}')
            return redirect('register')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used.')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match.')
            return redirect('register')
    else:
        return render(request, 'register.html')
    


def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Invalid username or password.')
                return redirect('login')
        except KeyError:
            messages.info(request, 'Please fill in all fields.')
            return redirect('login')
    else:
        return render(request, 'login.html')
    


def logout(request):
    auth.logout(request)
    return redirect('/')


def post(request, pk):
    return render(request, 'post.html', {'pk': pk})