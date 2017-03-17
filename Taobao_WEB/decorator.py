from django.http import HttpResponseRedirect,Http404
from django.shortcuts import redirect
from django.contrib.sessions.models import Session

def my_login_required(view_func):
    def wrapper(self, request):
        print request.session.session_key
        if Session.objects.filter(session_key=request.session.session_key).exists():
            return view_func(self,request)
        if Session.objects.all().count() > 0:
            raise Http404("Website is in use! Please Wait")
        else:
            return view_func(self, request)
    return wrapper