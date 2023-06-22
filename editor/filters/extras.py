import os
from django import template

register = template.Library()

@register.filter
def get_static_path(request,dl):

    print(" Current Directory ",os.getcwd())
    return "Hello World"