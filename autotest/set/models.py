from django.db import models

# Create your models here.


class Set(models.Model):
    setname = models.CharField('系统名称', max_length=200)
    setvalue = models.CharField('系统设置', max_length=200)

    class MATA:
        verbose_name = '系统设置'
        verbose_name_plural = '系统设置'

    def __str__(self):
        return self.setname