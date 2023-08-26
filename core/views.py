from django.shortcuts import render,redirect
from rest_framework.views import APIView
from core.models import Profile
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializer import *
from django.contrib.auth.models import User
import uuid
from .helpers import send_forgot_password_mail
from django.urls import reverse



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


def login_base(request):
    res = logout(request)
    return render(request,'base_site.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user, "user")
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'base_site.html', {'error_message': 'Invalid login'})

    return render(request, 'index.html')

def change_password(request,token):
    context={}
    # try:
    profile_obj=Profile.objects.filter(forget_password_token=token).first()
    print(profile_obj)
    print(profile_obj.user.id)
    if request.method=='POST':
        new_password=request.POST.get("password1")
        new_password2 = request.POST.get("password2")
        user_id= request.POST.get("user_id")
        if user_id is None:
            request.session['message'] = 'Invalid UserID'
            return redirect(f'/change_password/{token}')
        if new_password!=new_password2:
            request.session['message'] = 'Both Password should be equal'
            return redirect(f'/change_password/{token}')
        user_obj=User.objects.get(id=user_id)
        print(user_obj)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('/login')
    context={'user_id':profile_obj.user.id}
    # except Exception as e:
    #     print(e)
    return render(request,'change_password.html',context)


def logout_user(request):
	res=logout(request)
	response=render(request, 'base_site.html')
	return response

def forget_password(request):
    context={'success_message':''}
    # try:
    if request.method=='POST':
        username=request.POST.get("username")
        user_obj=User.objects.filter(username=username).first()
        print(user_obj,"user_obj")
        if user_obj:
            token=str(uuid.uuid4())
            profile_obj, created=Profile.objects.get_or_create(user=user_obj)
            print(profile_obj,"profile_obj")
            profile_obj.forget_password_token=token
            profile_obj.save()
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            port=request.META.get('SERVER_PORT', '')
            print(ip,"ip")
            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'
            send_forgot_password_mail(user_obj,token,protocol,ip,port)
            context["success_message"]="An Email link is sent to the registered email for verification, please change the password through the link "
        else:
            return render(request,'forgot_password.html', {'error_message':'Invalid Username'})
    # except Exception as e:
    #     print(e)
    return render(request,'forgot_password.html',context)