from django.contrib import admin
from product.models import Product
from apitest.models import Apis, Apitest
from apptest.models import Appcase
from webtest.models import Webcase
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'productname', 'productdesc', 'producter', 'create_time']


class Apisadmin(admin.TabularInline):
    list_display = [
        'apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult', 'apistatus', 'create_time', 'id', 'product'
    ]
    model = Apis
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'productname', 'productdesc', 'create_time', 'id'
    ]
    inlines = [Apisadmin]


class AppcaseAdmin(admin.TabularInline):
    list_display = ['appcasename', 'apptestresult', 'create_time', 'id', 'product']
    model = Appcase
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'productname', 'productdesc', 'create_time', 'id'
    ]
    inlines = [AppcaseAdmin]


class WebcaseAdmin(admin.TabularInline):
    list_display = ['webcasename', 'webcaseresult', 'create_time', 'id', 'product']
    model = Webcase
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc', 'create_time','id']
    inlines = [WebcaseAdmin]

admin.site.register(Product, ProductAdmin)
