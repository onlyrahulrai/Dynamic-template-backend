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

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    theme = models.ForeignKey(Theme,on_delete=models.SET_NULL,null=True,blank=True)

class Code(models.Model):
    name   = models.CharField(default="default",max_length=75)
    user   = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="codes")
    path   = models.CharField(max_length=200,null=True,blank=True)
    image  = models.ImageField(upload_to='directories',null=True,blank=True)
    public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Codes"




