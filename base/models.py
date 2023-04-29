from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Theme(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField(null=True,blank=True)
    slug = models.SlugField(null=True,blank=True)
    image = models.ImageField(upload_to='themes',null=True,blank=True)
    code = models.FileField(upload_to='codes',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Themes"

    def save(self,*args,**kwargs):
        self.slug = "-".join(self.name.lower().split(" "))
        return super().save(*args,**kwargs)

class Template(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='templates')
    header_code = models.TextField(null=True,blank=True)
    footer_code = models.TextField(null=True,blank=True)
    sidebar_code = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Templates"

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    theme = models.ForeignKey(Theme,on_delete=models.SET_NULL,null=True,blank=True)




