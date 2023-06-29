import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from config.settings import MEDIA_URL

User = get_user_model()


def search_friend(request):
    if request.method == 'GET':
        nickname = request.GET.get("nickname", '#')
        users = User.objects.filter(Q(username__icontains=nickname) & ~Q(username=request.user.username)).values('username', 'avatar')

        user_list = []
        for user in users:
            user_dict = {
                'username': user['username'],
                'avatar': MEDIA_URL + user['avatar'],
                'chat_room': reverse('chat:room', args=[user['username']])
            }
            user_list.append(user_dict)

        return JsonResponse({'users': user_list}, safe=False)


def add_friend(request, nickname):
    friend = get_object_or_404(User, username=nickname)
    request.user.friends.add(friend)
    return JsonResponse({'message': 'Додано'}, safe=False)
