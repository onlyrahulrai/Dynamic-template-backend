from django.shortcuts import render, get_object_or_404
from base.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .functions import get_templates_directory
from django.contrib.auth.decorators import login_required
import zipfile
from .decorators import *
from .functions import custom_render
import os
import shutil
from django.conf import settings

# Create your views here.

@decorate_func
def home(request):
    return custom_render(request,'code.html')

@login_required(login_url="/admin/login/")
def theme(request):
    themes = Theme.objects.all()

    context = {
        'themes': themes
    }

    return render(request, 'theme.html', context)

@csrf_exempt
def select_theme(request):
    if request.method == "POST":
        data = json.loads(request.body)

        theme = get_object_or_404(Theme, pk=data.get("id"))

        static_directory = os.path.join(settings.BASE_DIR,'static')

        user_static_directory = os.path.join(static_directory,request.user.username)

        template_directory = os.path.join(get_templates_directory(),request.user.username)

        with zipfile.ZipFile(theme.code.path, 'r') as zip_ref:
            zip_ref.extractall(template_directory)

            code_folder = os.listdir(template_directory)

            if request.user.username in os.listdir(static_directory):
                print(" User Static Directory ",user_static_directory)
                shutil.rmtree(user_static_directory)

            for item in code_folder:
                if item in ["css","js"]:
                    path = os.path.join(template_directory,item)

                    shutil.copytree(path,os.path.join(user_static_directory,item))

                    shutil.rmtree(path)

        if(request.user.is_authenticated):
            request.user.profile.theme = theme
            request.user.profile.save()

        return JsonResponse("Success", safe=False)
