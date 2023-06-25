import os
import shutil
import zipfile
from base.models import *
from django.conf import settings
from django.shortcuts import render, get_object_or_404


def get_templates_directory():
    for engine in settings.TEMPLATES:
        if 'DIRS' in engine:
            return engine['DIRS'][0]
    raise Exception('Templates directory not found in settings')


def custom_render(request, template):
    path = request.GET.get('path', 'live')
    user = request.GET.get('user', request.user.username)
    return render(request, f'{user}/{path}/{template}', {'path': path, 'username': user})


def get_theme(request=None, **kwargs):
    try:
        theme = get_object_or_404(Theme, pk=request.data.get(
            'id')) if request else Theme.objects.first()

        user = request.user if request else kwargs.get(
            "context").get("user")
        
        path = os.path.join(os.path.join(
            get_templates_directory(), user.username))

        if os.path.basename(path) not in os.listdir(get_templates_directory()):
            os.mkdir(path)

        template_directory = os.path.join(path, 'live')

        with zipfile.ZipFile(theme.code.path, 'r') as zip_ref:

            if os.path.basename(template_directory) in os.listdir(path):
                shutil.rmtree(template_directory)

            zip_ref.extractall(template_directory)

            code, created = Code.objects.get_or_create(
                name="live", user=user.profile, path=template_directory, public=True)

            code.image = theme.image

            code.save()

        return theme
    except SyntaxError as e:
        print(" Error ",e)
        raise SyntaxError("Couldn't Select Theme")
