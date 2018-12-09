from django.shortcuts import render
from product.models import Product
from django.contrib.auth.decorators import login_required
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def product_manage(request):
    username = request.session.get('user', '')
    product_list = Product.objects.all()
    paginator = Paginator.page(product_list, 8)
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1) # 如果输入的不是整数，返回page1
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages) # 如果输入的整数不在系统范围内,则显示最后一页数据
    product_count = Product.objects.all().count()
    return render(request, 'product_manage.html', {'user': username, 'products': product_list,
                                                   'productcounts': product_count})

# 搜索功能
@login_required
def productsearch(request):
    username = request.session.get('user', '')
    search_productname = request.GET.get("productname", "")
    regx = '^\d+$'
    if search_productname != '':
        if re.search(regx,search_productname) != None:
            product_list = Product.objects.filter(id=search_productname)
        else:
            product_list = Product.objects.filter(productname__icontains=search_productname,)
        return render(request, 'product_manage.html', {"user": username, "products": product_list})
    else:
        product_list = Product.objects.all()
        return render(request, 'product_manage.html', {"user": username, "products": product_list})


    

