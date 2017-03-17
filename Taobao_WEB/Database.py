from django.contrib.auth.models import User
from pymongo import MongoClient
import time

def database(query_name,module_name,status):
    db = MongoClient()['Project']
    db.history.insert({'Query Name':query_name,
                       'TimeStamp':time.localtime(),
                       'Module_used':module_name,
                       'Status':status,
                       })
    MongoClient().close()
def get_profile_data(request):
    user = User.objects.get(username=request.session['username'])
    context = {
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined

    }
    return context


def save_details(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.get(username=request.session['username'])
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.set_password(password)
    user.save()
