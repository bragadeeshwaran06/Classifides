from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ads.models import Ad  
from .forms import CustomUserCreationForm
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email is already in use')
            else:
                user = form.save()  
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)  
                login(request, user) 
                return redirect('home') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    ads = Ad.objects.filter(user=user)  
    return render(request, 'user_profile.html', {'user': user, 'ads': ads})

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

class CustomPasswordResetView(PasswordResetView):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')  
        return super().dispatch(*args, **kwargs)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home') 
        return super().dispatch(*args, **kwargs)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home') 
        return super().dispatch(*args, **kwargs)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')  
        return super().dispatch(*args, **kwargs)

def custom_logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)
    else:
        return redirect('/')
