from django.shortcuts import render, HttpResponse, redirect
from .models import UserProfile, Friends, Messages
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from aso.serializers import MessageSerializer
from django.contrib.auth.models import Group
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = UserProfile.objects.get(username=username)
    id = use.id
    return id


def index(request):
    """
    Return the home page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "aso/index.html", {})
    else:
        postpage = PostPage.objects.all()
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
        context = {'postpage':postpage, 'friends':friends}
        return render(request, "aso/main.html",context)


def search(request):
    """
    Search users page
    :param request:
    :return:
    """
    users = list(UserProfile.objects.all())
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break

    if request.method == "POST":
        print("SEARCHING!!")
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.name or query in user.username:
                user_ls.append(user)
        return render(request, "aso/search.html", {'users': user_ls, })

    try:
        users = users[:10]
    except:
        users = users[:]
    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    return render(request, "aso/search.html", {'users': users, 'friends': friends})


def addFriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """

    username = request.user.username
    id = getUserId(username)
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("/search")


@login_required(login_url='login')
def chat(request, username):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    friend = UserProfile.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = UserProfile.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "aso/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})


@login_required(login_url='login')
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@login_required(login_url='login')
def main(request):
    postpage = PostPage.objects.all().order_by('-id')
    context = {'postpage':postpage}
    return render(request, 'aso/main.html', context)

@login_required(login_url='login')
def myaccount(request):
    user = UserProfile.objects.get(username=request.user.username)
    form = PostPageForm()
    print(user.name)
    if request.method == "POST":
        form = PostPageForm(request.POST,request.FILES)
        if form.is_valid():
            x=form.save()
            x.user=request.user
            x.save()
            return redirect('main')
    context = {'user':user, 'form':form}
    return render(request, 'aso/myaccount.html',context)

@login_required(login_url='login')
def chatRoom(request,username):
    chatroom=ChatRoom.objects.get(username=username)
    gr=Group.objects.get(name=username)
    #print("my groups ",request.user.groups.all())
    if not (gr  in request.user.groups.all()) :
        return redirect('/access_denied/'+username)

    #rooms=ChatRoom.objects.all()
    members = User.objects.filter(groups__name=gr.name)
    messages=ChatMessage.objects.filter(chat_room=chatroom)
    room_name=chatroom.name
    context={'messages':messages,'members':members,"room_name":room_name}
    if request.method=='POST':
        text=request.POST.get('message')
        tg=text.replace(' ','')
        x=True
        if not tg:
            x=False
            
        print('user',request.user)
        try:
            te=ChatMessage.objects.filter(user=request.user).last().text
        except:
            
            te=''
            
        if te != text and x:
            ChatMessage.objects.create(user=request.user,chat_room=chatroom,text=text)
    return render(request, "aso/chatroom.html",context)

def access_denied(request,username):
    admin=ChatRoom.objects.get(username=username).user
    context={'admin':admin}
    return render(request,'aso/access_denied.html',context)

@login_required(login_url='login')
def create_room(request):
    form=ChatCreationForm()
    if request.method=='POST':
        form=ChatCreationForm(request.POST,request.FILES)
        if form.is_valid():
            x=form.save(commit=False)
            x.user=request.user
            x.save()
            

            return redirect('/invite_user/'+x.username)

    context={'forms':form}
    return render(request, "aso/registerroom.html",context)

@login_required(login_url='login')
def chatrooms(request):
    rooms=ChatRoom.objects.order_by('-date')
    x=request.user.groups.all()
    print(x)
    context={'rooms':rooms}
    return render(request, "aso/rooms_to.html",context)


@login_required(login_url='login')
def inviteuser(request,username):
    #listofinvited=[]
    room=ChatRoom.objects.get(username=username)
    gr=Group.objects.get(name=room.username)
    
    inviteds = User.objects.filter(groups__name=gr.name)
    uninviteds = User.objects.filter(~Q(groups__name=gr.name)).order_by('-id')
    print("invited",inviteds)
    print("uninvited",uninviteds)
    if request.method=="POST":
        sear=request.POST.get("search")
        sear=sear.replace("@","")
        uninviteds=User.objects.filter(~Q(groups__name=gr.name)).filter(Q( username__icontains=sear))
    context={'inviteds':inviteds,'uninviteds':uninviteds,'pk':username}

    return render(request, "aso/addedlist.html",context)

@login_required(login_url='login')
def invited(request,username,chat):
    gr=Group.objects.get(name=username)
    user=User.objects.get(username=chat)
    gr.user_set.add(user)
    return redirect('/invite_user/'+username)

def deleteRoom(request, username):
    room = ChatRoom.objects.get(username=username)
    group = Group.objects.get(name=username)
    if request.method == 'POST':
        room.delete()
        group.delete()
        return redirect('chatrooms')
    context = {'room':room}
        
    return render(request, 'aso/delete_group.html',context)
