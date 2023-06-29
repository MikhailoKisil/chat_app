from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_friends(request):
    if request.user.is_authenticated:
        user_friends = request.user.friends.all()
        to_user_msgs = request.user.messages_to_me.all()
        for friend in user_friends:
            friend.unread_msgs = len([i for i in to_user_msgs if i.from_user_id == friend.pk and i.read == False])
        return {'user_friends': user_friends}
    return {'user': request.user}
