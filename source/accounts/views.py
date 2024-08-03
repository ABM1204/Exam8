from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .forms import CustomUserCreationForm

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'accounts/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'accounts/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
