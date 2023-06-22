from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from base.models import *
from .decorators import *
from .functions import get_templates_directory
from .functions import custom_render
import json
import os
import shutil
import zipfile

# Create your views here.
@decorate_func
def home(request):
    return custom_render(request,f'code.html')

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

        # static_directory = os.path.join(settings.BASE_DIR,'static')

        # user_static_directory = os.path.join(static_directory,request.user.username)


        template_directory = os.path.join(os.path.join(get_templates_directory(),request.user.username),'live')

        with zipfile.ZipFile(theme.code.path, 'r') as zip_ref:
            
            if request.user.username in os.listdir(get_templates_directory()):
                shutil.rmtree(template_directory)

            zip_ref.extractall(template_directory)

            code,created = Code.objects.get_or_create(name="live",user=request.user.profile,path=template_directory,public=True)

            code.image = theme.image

            code.save()

            # code_folder = os.listdir(template_directory)

            # if request.user.username in os.listdir(static_directory):
            #     shutil.rmtree(user_static_directory)

            # for item in code_folder:
            #     if item in ["css","js"]:
            #         path = os.path.join(template_directory,item)

            #         shutil.copytree(path,os.path.join(user_static_directory,item))

            #         shutil.rmtree(path)

        if(request.user.is_authenticated):
            request.user.profile.theme = theme
            request.user.profile.save()

        return JsonResponse("Success", safe=False)
