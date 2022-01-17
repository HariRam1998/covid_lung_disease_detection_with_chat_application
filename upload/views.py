from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
import cloudinary.uploader
from django.contrib.auth import login as user_login
from django.contrib import messages
import cloudinary
import requests
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from upload.models import Message
from upload.serializers import MessageSerializer, UserSerializer


from django.views.decorators.csrf import csrf_exempt

# Create your views here.
cloudinary.config(cloud_name='df4siptjs', api_key='727231952262334',
                  api_secret='f8WYhe1BrWJNwbE4lCq9pP0hpJM')


def covidlung(request):
    url12 = None
    # if request.user.is_authenticated:
    #     url12 = request.user.first_name
    #
    if request.POST:
        return _extracted_from_covidlung_10(request, url12)
    # context = {
    #     'proimage': url12,
    #     'notification': Notification.objects.filter(receiver=request.user.username),
    #     'pagetitle': 'Covid lung',
    # }
    return render(request, 'fileupload.html')


def _extracted_from_covidlung_10(request, url12):
    file = request.FILES['files']
    upload_result = cloudinary.uploader.upload(file)
    url = upload_result['url']
    URL = 'https://covidlungsdetection.herokuapp.com/?link=' + url
    response = requests.get(URL)
    data = response.json()
    print(data["predict"])
    context = {
        'proimage': url12,
        'predict': data["predict"],
        'url': url,
        'pagetitle': 'Covid Analysis',
    }
    return render(request, 'prediction.html', context)


# def _extracted_from_covidlung_10(request, url12):
#     file = request.FILES['files']
#     upload_result = cloudinary.uploader.upload(file)
#     url = upload_result['url']
#     URL = 'https://covidlungsdetection.herokuapp.com/?link=' + url
#     response = requests.get(URL)
#     data = response.json()
#     print(data["predict"])
#     context = {
#         'proimage': url12,
#         'predict': data["predict"],
#         'url': url,
#         'notification': Notification.objects.filter(receiver=request.user.username),
#         'pagetitle': 'Covid Analysis',
#     }
#     return render(request, 'prediction.html', context)

def login1(request):
    if request.POST:
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')
        if User.objects.filter(username__iexact=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user_login(request, user)
                return redirect('chats')
            else:
                messages.warning(request, "Password is Wrong!!")
        else:
            messages.warning(request, "Username is Wrong!!")

    return render(request, 'login.html', {})


def register(request):
    if request.POST:
        username = request.POST.get('register_username')
        email = request.POST.get('register_email')
        password = request.POST.get('register_password')
        print(username)
        print(email)
        print(password)

        if (User.objects.filter(username__iexact=username).exists() == False and User.objects.filter(
                email__iexact=email).exists() == False):
            return _extracted_from_register_10(username, email, password, request)
        elif User.objects.filter(username__iexact=username).exists():
            messages.warning(request, "Username Already exists!!")

        elif User.objects.filter(email__iexact=email).exists():
            messages.warning(request, "Email Already exists!!")

    return render(request, 'login.html')


def _extracted_from_register_10(username, email, password, request):
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    user = User.objects.get(username=username)
    message = 'You have sucessfully registered!!!'
    return redirect('user_login')


def logoutfun(request):
    print("hey")
    logout(request)
    return redirect('user_register')


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


# @csrf_exempt
# def message_list(request, sender=None, receiver=None):
#     """
#     List all required messages, or create a new message.
#     """
#     # if request.method == 'GET':
#         # messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
#         # serializer = MessageSerializer(messages, many=True, context={'request': request})
#         # for message in messages:
#         #     message.is_read = True
#         #     message.save()
#         # return JsonResponse(serializer.data, safe=False)
#
#     # elif request.method == 'POST':
#         # data = JSONParser().parse(request)
#         # serializer = MessageSerializer(data=data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return JsonResponse(serializer.data, status=201)
#         # return JsonResponse(serializer.errors, status=400)
#     return redirect('covidlung')


def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        # if user is not None:
        #     login(request, user)
        # else:
        #     return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')

# def message_view(request, sender, receiver):
#     if not request.user.is_authenticated:
#         return redirect('index')
#     if request.method == "GET":
#         return render(request, "chat/messages.html") #,
#         #               {'users': User.objects.exclude(username=request.user.username),
#         #                'receiver': User.objects.get(id=receiver),
#         #                'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
#         #                            Message.objects.filter(sender_id=receiver, receiver_id=sender)})
#
#
#

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


def user_home(request):
    return render(request,'home.html',{})