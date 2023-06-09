from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","first_name","last_name","email"]
