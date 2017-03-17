from django.shortcuts import render,loader,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate, login,logout,user_logged_in
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.models import User
from email.mime.multipart import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib
from email.mime.text import MIMEText
import threading
from django.contrib.auth.decorators import login_required
from .decorator import my_login_required
from django.contrib.sessions.models import Session


search_name = ""
email = ""

class ABC(View):
    def get(self, request):
        Session.objects.all().delete()


class Index(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        else:
            #print (Session.session_key)
            return render(request, 'home.html')


class Search_Items(View):
    @my_login_required
    def get(self, request):
        return render(request, 'Search_Items.html')


class Search_Results(View):
    @my_login_required
    def post(self, request):
        if 'search_name' in request.POST:
            global search_name
            search_name = request.POST['search']
            return render(request, 'search.html')

        elif 'get_email' in request.POST:
            global email
            email = request.POST['email']
            t = threading.Thread(target=background_process, args={}, kwargs={})
            t.start()
            return render(request, 'results.html')


class Profile(View):
    @my_login_required
    def get(self, request):
        user = User.objects.get(username=request.user)

        context = {
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined

        }
        return render(request, 'profile.html',context)

class EditInfo(View):
    @my_login_required
    def get(self, request):
        return render(request, 'edit_info.html')

    @my_login_required
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=request.user)
        user.username = username
        user.set_password(password)
        user.save()
       
        return render(request, 'profile.html')


class Logout(View):
    def get(self,request):
        logout(request)
        #print request.session.session_key
        form = UserForm(request.POST or None)
        context = {
            "form": form,
        }
        return redirect('index')

class Login(View):
    @my_login_required
    def post(self,request):
        #print "123456789"
        username = request.POST['username']
        password = request.POST['password']
        #print password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'home.html')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid login'})
        return render(request, 'login.html')

class SignUp(View):
    @my_login_required
    def get(self, request):
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'home.html', {})
        context = {
            "form": form,
        }
        return render(request, 'signup.html', context)

def email_data(email, search):
    msg = MIMEMultipart()
    msg.attach(MIMEText(search+"\nThis is the data"))
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("manage.py", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="WorkBook3.xlsx"')
    msg.attach(part)

    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.starttls()
    mail.ehlo()
    mail.login('nishafnaeem3@gmail.com', 'lapetitemorte1')
    mail.sendmail("nishafnaeem3@gmail.com", email, msg.as_string())
    mail.quit()

import time
def background_process():
    time.sleep(15)
    #print"Nishaf"
    #print "heloo"
    email_data(email, search_name)






