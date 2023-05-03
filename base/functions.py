from django.conf import settings
from django.shortcuts import render

def get_templates_directory():
    for engine in settings.TEMPLATES:
        if 'DIRS' in engine:
            return engine['DIRS'][0]
    raise Exception('Templates directory not found in settings')

def custom_render(request,template):
    return render(request,f'{request.user.username}/{template}')