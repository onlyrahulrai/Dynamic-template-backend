from django.shortcuts import render, get_object_or_404
from base.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .functions import get_templates_directory
from django.contrib.auth.decorators import login_required
import zipfile
from .decorators import *
import os

# Create your views here.

@decorate_func
def home(request):
    return render(request,f"{request.user.username}/code.html")

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

        print(" Path ",theme.code.url)

        template_dir = os.path.join(get_templates_directory(),request.user.username)

        with zipfile.ZipFile(theme.code.path, 'r') as zip_ref:
            zip_ref.extractall(template_dir)

        if(request.user.is_authenticated):
            request.user.profile.theme = theme
            request.user.profile.save()

        return JsonResponse("Success", safe=False)
