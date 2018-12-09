from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from webtest.models import Webcase, Webcasestep
import re
from django.db.models import Q
# Create your views here.


#Web 用例管理
@login_required
def webcase_manage(request):
    webcase_list = Webcase.objects.all()
    username = request.session.get('user', '')
    return render(request, "webcase_manage.html", {'user':username, 'webcases': webcase_list})

#Web 用例测试步骤
@login_required
def webcasestep_manage(request):
    username = request.session.get('user', '')
    webcasestep_list = Webcasestep.objects.all()
    return render(request, "webcasestep_manage.html", {'user': username, 'webcasesteps':webcasestep_list})



@login_required
def websearch(request):
    username = request.session.get('user', '')
    search_webcasename = request.GET.get("webcasename", "")
    regx = '^\d+$'
    if search_webcasename != '':
        if re.search(regx, search_webcasename) != None:
            searchQ = Q(id=search_webcasename)|Q(webcasename__icontains=search_webcasename)
            webcase_list = Webcase.objects.filter(searchQ)
        else:
            webcase_list = Webcase.objects.filter(webcasename__icontains=search_webcasename)
    else:
        webcase_list = Webcase.objects.all()
    return render(request, 'webcase_manage.html', {"user": username, "webcases": webcase_list})



@login_required
def webstepsearch(request):
    username = request.session.get('user', '')
    search_webcasename = request.GET.get("webcasename", "")
    regx = '^\d+$'
    if search_webcasename != '':
        if re.search(regx, search_webcasename) != None:
            searchQ = Q(id=search_webcasename)|Q(Webcase__webcasename__icontains=search_webcasename)
            webcasestep_list = Webcasestep.objects.filter(searchQ)
        else:
            webcasestep_list = Webcasestep.objects.filter(webcasename__icontains=search_webcasename)
    else:
        webcasestep_list = Webcasestep.objects.all()
    return render(request, 'webcasestep_manage.html', {"user": username, "webcasesteps": webcasestep_list})
