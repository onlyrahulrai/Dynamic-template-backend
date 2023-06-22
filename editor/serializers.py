from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from base.models import *


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","first_name","last_name","email"]

class CodeDirectorySerializer(ModelSerializer):
    class Meta:
        model = Code
        fields = ['id','name','user','path','public','image']

class ThemeSerializer(ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id','name','description','slug','image','created_at','updated_at']