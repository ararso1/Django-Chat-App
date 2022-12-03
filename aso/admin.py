from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Messages)
admin.site.register(Friends)
admin.site.register(PostPage)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)