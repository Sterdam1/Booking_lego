from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserProfileForm, CustomUserCreationForm
from .models import Profile, NewField
from django.contrib.auth.models import User
from main import DataBase, DataBaseBooking

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
        # Если пользователь аутентифицирован, показываем домашнюю страницу
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid(): # and profile_form.is_valid():
            # user = 
            user_form.save()
            user = dict(user_form.data)
            user_id = User.objects.get(username=user['username'][0])
            profile = Profile.objects.create(user=user_id, username=user['username'][0], email=user['email'][0], password=user['password1'][0])
        
            return redirect('login')  
        
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'singin.html', {'form': user_form,})#'profile_form': profile_form, 'error_message': request.method})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page.
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def create_event(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    all_fields = [i.field_name for i in NewField.objects.filter(created_by=request.user.id)]

    return render(request, 'create_event.html',{'fields': all_fields})

def create_event_conformation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    fields = [i.field_name for i in NewField.objects.filter(created_by=request.user.id)]
    try:
        db_book = DataBaseBooking()
        db_book.create_table(fields, request.user.username)
        return render(request, 'create_event_conformation.html',{'message': "Успех"})
    except Exception as e:
        return render(request, 'create_event_conformation.html',{'message': e})
