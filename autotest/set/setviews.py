from django.shortcuts import render
from set.models import Set
from django.contrib.auth.admin import User
import re
from django.contrib.auth.decorators import login_required

# Create your views here.

# 系统管理
def set_manage(request):
    username = request.session.get('user', '')
    set_list = Set.objects.all()
    return render(request, "set_manage.html", {"user": username, "sets": set_list})

# 用户管理功能
def set_user(request):
    user_list = User.objects.all()
    username = request.session.get('user', '')
    return render(request, "set_user.html", {"user": username, "users":user_list})

# 搜索功能
@login_required
def setsearch(request):
    username = request.session.get('user', '')
    search_setname = request.GET.get("setname", "")
    regx = '^\d+$'
    if re.search(regx,search_setname) != None:
        set_list = Set.objects.filter(id=search_setname)
        return render(request, 'set_manage.html', {'user':username, 'sets':set_list})

    else:
        set_list = Set.objects.filter(setname__icontains=search_setname,)
        return render(request, 'set_manage.html', {"user": username, "sets": set_list})

