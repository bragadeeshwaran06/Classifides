from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ads.models import Ad  
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
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

@require_http_methods(["GET", "POST"])
def custom_logout_view(request):
    logout(request)
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)