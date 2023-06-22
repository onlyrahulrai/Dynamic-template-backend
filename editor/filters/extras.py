import os
from django import template

register = template.Library()

@register.filter
def get_static_path(request,path):
    path = request.GET.get('path','live')
    user = request.GET.get('user',request.user.username)
    return f'/{user}/{path}'