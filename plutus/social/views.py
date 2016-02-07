from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from . import models
import json


# Create your views here.


def auth_sess(session_key):
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    return user;


def getUsers(request):
    

    x = User.objects.all()
    
    ret = {}
    count = 0
    for usr in x:
        
        ret[count] = {}
        
        pts = 0
        try:
            pts = models.Achievments.objects.get(primary_key=usr.id).points
        except Exception:
            ret[count]['score'] = pts 
            ret[count]['name'] = usr.username        
            ret[count]['id'] = usr.id    
            
        ret[count]['score'] = pts 
        ret[count]['name'] = usr.username
        ret[count]['id'] = usr.id
        count = count + 1;
    
    return HttpResponse(json.dumps(ret))
        
        
def getMyPoints(request):
    
    usr = auth_sess(request.GET['sessionid'])
    
    if usr.is_authenticated():
        pts = models.Achievments.objects.get(primary_key=usr.id).points
        
        
        return HttpResponse(pts)

def userInfo(request):
    
    uid = request.GET['uid']
    
    user = User.objects.get(id=uid)
    
    returnval = {}
    
    returnval['id'] = user.id
    returnval['score'] = 1
    returnval['name'] = user.username
    returnval['achievments'] = 1
  
        
    return HttpResponse(json.dumps(returnval))