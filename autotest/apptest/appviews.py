from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login
from apptest.models import Appcase, Appcasestep
import re
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.


#app用例管理
@login_required
def appcase_manage(request):
    appcase_list = Appcase.objects.all()
    username = request.session.get('user', '')
    return render(request, "appcase_manage.html", {"user":username, "appcases":appcase_list})


#app用例步骤
@login_required
def appcasestep_manage(request):
    username = request.session.get('user', '')
    appcasestep_list = Appcasestep.objects.all()
    return render(request, "appcasestep_manage.html", {'user': username, 'appcasesteps': appcasestep_list})


# 搜索功能，通过正则匹配，按照ID 或者appcase名称搜索
@login_required
def appsearch(request):
    username = request.session.get('user', '')
    search_appcasename = request.GET.get("appcasename", "")

    regx = '^\d+$'
    if search_appcasename != '':
        if re.search(regx,search_appcasename) != None:
            sqlQ = Q(id=search_appcasename)|Q(appcasename__icontains=search_appcasename)
            appcase_list = Appcase.objects.filter(sqlQ)
        else:
            appcase_list = Appcase.objects.filter(appcasename__icontains=search_appcasename,)
    else:
        appcase_list = Appcase.objects.all()

    return render(request, 'appcase_manage.html', {"user": username, "appcases": appcase_list})


'''
    searchQ = Q(id=search_appcasename)|Q(appcasename__icontains=search_appcasename)
    if search_appcasename != '':
        appcase_list = Appcase.objects.filter(searchQ)
    else:
        appcase_list = Appcase.objects.all()
    return render(request, 'appcase_manage.html', {"user": username, "appcases": appcase_list})
'''


@login_required
def appstepsearch(request):
    username = request.session.get('user', '')
    search_appcasename = request.GET.get("appcasename", "")
    regx = '^\d+$'
    if search_appcasename != '':
        if re.search(regx, search_appcasename) != None:
            searchQ = Q(id=search_appcasename)|Q(Appcase__appcasename__icontains=search_appcasename)
            appcasestep_list = Appcasestep.objects.filter(searchQ)
        else:
            appcasestep_list = Appcasestep.objects.filter(Appcase__appcasename__icontains=search_appcasename)
    else:
        appcasestep_list = Appcasestep.objects.all()
    return render(request, 'appcasestep_manage.html', {"user": username, "appcasesteps": appcasestep_list})

