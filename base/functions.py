from django.conf import settings
from django.shortcuts import render

def get_templates_directory():
    for engine in settings.TEMPLATES:
        if 'DIRS' in engine:
            return engine['DIRS'][0]
    raise Exception('Templates directory not found in settings')

def custom_render(request,template):
    path = request.GET.get('path','live')
    user = request.GET.get('user',request.user.username)
    return render(request,f'{user}/{path}/{template}',{'path':path,'username':user})