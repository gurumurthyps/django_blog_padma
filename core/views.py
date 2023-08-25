from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializer import *
from django.contrib.auth.models import User
import uuid
from .helpers import send_forgot_password_mail


# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin






class ReactView(APIView):
    serializer_class = ReactSerializer

    def get(self, request):
        detail = [{"name": detail.name, "detail": detail.detail}
                  for detail in React.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


def main_dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'base_site.html')
    else:
        context={}
        return render(request, 'index.html', context)


def login(request):
    return render(request,'base_site.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'base_site.html', {'error_message': 'Invalid login'})

    return render(request, 'index.html')



def logout_user(request):
	res=logout(request)
	response=render(request, 'base_site.html')
	return response

def forget_password(request):
    try:
        if request.method=='POST':
            username=request.POST.get("username")
            user_obj=User.objects.filter(username=username).first()
            if user_obj:
                token=str(uuid.uuid4())
                send_forgot_password_mail(user_obj,token)
            else:
                return render(request,'forgot_password.html', {'error_message':'Invalid Username'})
    except Exception as e:
        print(e)
    return render(request,'forgot_password.html')