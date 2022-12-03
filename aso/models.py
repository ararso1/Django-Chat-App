from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import Group

class UserProfile(models.Model):

    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"


class Messages(models.Model):

    description = models.TextField()
    sender_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)


class Friends(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"

class PostPage(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
	    return self.text


class ChatRoom(models.Model):
        user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
        name=models.CharField(max_length=30)
        username=models.CharField(unique=True,max_length=20)
        date = models.DateTimeField(auto_now_add=True, blank=True,null=True)

        def __str__(self):
            return self.name
        def save(self, *args, **kwargs):
            try:
                l=ChatRoom.objects.get(username=self.username)
                print("my chat",l)
            except:
                print("working")
                gr=Group.objects.create(name =self.username)
                print("my-user",self.user)
                user=User.objects.get(username=self.user.username)
                user.groups.add(gr)
                
            
            return super().save(*args, **kwargs)
class ChatMessage(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    chat_room=models.ForeignKey(ChatRoom,null=True, blank=True, on_delete=models.CASCADE)
    text=models.CharField(max_length=800)
    image = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
            return self.user.username + self.text[:10]