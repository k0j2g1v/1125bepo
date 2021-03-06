from IPython import embed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm


# Create your views here.

# Authentication(인증) -> 신원 확인
#   - 자신이 누구라고 주장하는 사람의 신원을 확인하는 것

def signup(request):
  if request.user.is_authenticated:
    return redirect('articles:index')

  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    # embed()
    if form.is_valid():
      user = form.save()
      auth_login(request, user)
      return redirect('articles:index')
  else:
    form = CustomUserCreationForm()
  context = {'form' : form}
  return render(request, 'accounts/signup.html', context)

def login(request):
  if request.user.is_authenticated:
    return redirect('articles:index')

  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      auth_login(request, form.get_user())
      return redirect('articles:index')
  else:
    form = AuthenticationForm()
  context = {'form' : form}
  return render(request, 'accounts/login.html', context)

def logout(request):
  auth_logout(request)
  return redirect('articles:index')

def profile(request, username):
  person = get_object_or_404(get_user_model(), username=username)
  context = {'person' : person}
  return render(request, 'accounts/profile.html', context)

