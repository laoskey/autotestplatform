from product.models import Product
from django.db import models


# Create your models here.
class Apitest(models.Model):
    Product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True)
    # 关联产品ID，product 是应用名称，Product是product应用的表名
    apitestname = models.CharField('流程接口名称', max_length=64)
    apitestdesc = models.CharField('流程接口描述', max_length=64, null=True)
    apitester = models.CharField('测试负责人', max_length=16)
    apitestresult = models.BooleanField('测试结果')
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        verbose_name = '流程接口场景'
        verbose_name_plural = '流程场景接口'

    def __str__(self):
        return self.apitestname


class Apistep(models.Model):
    Apitest = models.ForeignKey('Apitest', on_delete=models.CASCADE)
    apiname = models.CharField('接口名称', max_length=100)
    apiurl = models.CharField('URL地址', max_length=200)
    apiparamvalue = models.CharField('请求参数和值', max_length=800)
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'), ('delete', 'delete'), ('patch', 'patch'))
    apimethod = models.CharField('请求方法', choices=REQUEST_METHOD, default='get', max_length=200, null=True)
    apiresult = models.CharField('预期结果', max_length=200)
    apistatus = models.BooleanField('是否通过')
    create_time = models.DateTimeField('创建时间', auto_now=True)


class Apis(models.Model):
    # 关联产品ID
    Product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True)
    apiname = models.CharField('接口名称', max_length=100)
    apiparamvalue = models.CharField('请求参数和值', max_length=800)
    apiurl = models.CharField('url地址', max_length=200)
    REQUEST_METHOD = (('0', 'get'), ('1', 'post'), ('2', 'put'), ('3', 'delete'), ('4', 'patch'))
    apimethod = models.CharField(verbose_name='请求方法', choices=REQUEST_METHOD, default='0', max_length=200)
    apiresult = models.CharField('预期结果', max_length=200)
    apistatus = models.BooleanField('是否通过')
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        verbose_name = '单一场景接口'
        verbose_name_plural = '单一场景接口'

    def __str__(self):
        return self.apiname









def __str__(self):
    return self.name

