import json
import redis

from django.contrib.auth import logout, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe

from chat.forms import RegisterUserForm
from config import settings

User = get_user_model()

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)
def index(request):
    if request.user.is_authenticated:
        return redirect('chat:chat')
    else:
        return render(request, "chat/index.html")


@login_required
def chat(request):
    return render(request, 'chat/chat.html')


@login_required
def room(request, other_username):
    other_user = get_object_or_404(User, username=other_username)
    room_name = "_".join(sorted([request.user.username, other_user.username]))
    context = {
        "other_user": other_user,
        "room_name": room_name
    }
    return render(request, "chat/room.html", context)


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            redis_instance.set(user.pk, 'Offline')
            return redirect('chat:chat')
    else:
        form = RegisterUserForm()
    return render(request, 'chat/account/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('chat:chat')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/account/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('chat:index')


def user_status(request, user_pk):
    status = redis_instance.get(user_pk)
    if status:
        status = status.decode('utf-8')
    else:
        status = 'Offline'
    return JsonResponse({'status': status}, safe=False)


