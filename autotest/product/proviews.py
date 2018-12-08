from django.shortcuts import render
from product.models import Product
from django.contrib.auth.decorators import login_required
import re
# Create your views here.

def product_manage(request):
    username = request.session.get('user', '')
    product_list = Product.objects.all()
    return render(request, 'product_manage.html', {'user':username, 'products':product_list})

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


    

