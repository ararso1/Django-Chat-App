from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path("index", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("addfriend/<str:name>", views.addFriend, name="addFriend"),
    path("chat/<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    
    path('myaccount', views.myaccount, name='myaccount'),
    path("chat_room/<str:username>", views.chatRoom, name="chatroom"),
    path("create_chat_room",views.create_room,name="createchatroom"),
    path("chatrooms",views.chatrooms,name="chatrooms"),
    path("invite_user/<str:username>",views.inviteuser,name="invite"),
    path("invite/<str:username>/<str:chat>", views.invited, name="invited"),
    path("access_denied/<str:username>/",views.access_denied,name="access_denied"),
    path("delete_room/<str:username>", views.deleteRoom, name="delete_room"),

]
