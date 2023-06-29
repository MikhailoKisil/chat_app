from django.contrib import admin
from django.contrib.auth import get_user_model

from chat.models import Message, Conversation

User = get_user_model()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )
    list_display_links = ('username',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    pass
