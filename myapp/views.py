from django.shortcuts import render_to_response, get_object_or_404
import random, string, json
from myapp.models import urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.context_processors import csrf
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re
import hashlib
import urllib2, urllib

ARR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base(num, array=ARR):
    if(num==0):
        return array[0]
    retarr=[]
    base = len(array)
    while num:
        num, res = divmod(num,base)
        retarr.append(array[res])
    retarr.reverse()
    return ''.join(retarr)[:6]

def validate_number(num):
    pattern = re.compile("^\d{10}$",re.IGNORECASE)
    return pattern.match(num) is not None

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html', c)
 
def shorten_url(request):
     team = request.POST.get("teamname", '')
     p1 = request.POST.get("c1", '')
     p2 = request.POST.get("c2", '')
     cont = request.POST.get("phone", '')
     error_data={}
     error_data['err'] = "Blank field(s)"
     if team=='' :
        return HttpResponse(json.dumps(error_data), content_type="application/json")
     if p1=='' :
        return HttpResponse(json.dumps(error_data), content_type="application/json")
     if p2=='' :
        return HttpResponse(json.dumps(error_data), content_type="application/json")
     if cont=='' :
        return HttpResponse(json.dumps(error_data), content_type="application/json")
     alphanum=team + cont
     team_name = urls.objects.filter(teamname=team)
     if team_name.count()>=1:
        error_data['err'] = "Team name already exists!"
        return HttpResponse(json.dumps(error_data), content_type="application/json")
     if not validate_number(cont):
        error_data['err'] = "Please enter a valid number!"
        return HttpResponse(json.dumps(error_data), content_type="application/json")
     short = (hashlib.md5(alphanum.encode())).hexdigest()
     short = int(short,16)
     short = encode_base(short)
     b = urls(teamname=team, short_id=short,contestant1=p1,contestant2=p2,contact=cont)
     b.save()
     auth_key = '144872AoGnBaVgqLh59f59619'
     message = 'Your unique team ID for JCC 2017 is ' + short + '. Kindly take note and submit this at the event.'
     data = {
        'authkey':auth_key,
        'mobiles':cont,
        'message':message,
        'sender':'GNULUG',
        'route':'4',
     }
     url = 'http://sms.globehost.com/api/sendhttp.php?'
     req = urllib2.Request(url,urllib.urlencode(data));
     response = urllib2.urlopen(req)
     result = response.read().decode()
     response_data = {}
     response_data['uid'] = short
     return HttpResponse(json.dumps(response_data),  content_type="application/json")
        #return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")