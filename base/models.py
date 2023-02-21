from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='data')
    header = models.TextField(null=True,blank=True)
    footer = models.TextField(null=True,blank=True)
    sidebar = models.TextField(null=True,blank=True)

class Template(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='templates')
    header_code = models.TextField(null=True,blank=True)
    footer_code = models.TextField(null=True,blank=True)
    sidebar_code = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Templates"
