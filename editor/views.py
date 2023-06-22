import os
import shutil
from django.shortcuts import get_object_or_404
from .utils import display_tree
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserDetailSerializer,
    CodeDirectorySerializer,
    ThemeSerializer
)
from base.models import *
from rest_framework import status
from base.functions import get_templates_directory
from django.db import transaction
import os
import shutil
import zipfile

# Create your views here.


class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        print(" Id ", request.GET.get('id'))

        code = get_object_or_404(Code, pk=request.GET.get('id'))
        folder = display_tree(code.path)
        return Response(folder)


class ThemeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        themes = Theme.objects.all()
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            theme = get_object_or_404(Theme, pk=request.data.get("id"))

            path = os.path.join(os.path.join(
                get_templates_directory(), request.user.username))

            if os.path.basename(path) not in os.listdir(get_templates_directory()):
                os.mkdir(path)

            template_directory = os.path.join(path, 'live')

            with zipfile.ZipFile(theme.code.path, 'r') as zip_ref:

                if os.path.basename(template_directory) in os.listdir(path):
                    shutil.rmtree(template_directory)

                zip_ref.extractall(template_directory)

                code, created = Code.objects.get_or_create(
                    name="live", user=request.user.profile, path=template_directory, public=True)

                code.image = theme.image

                code.save()

            if(request.user.is_authenticated):
                request.user.profile.theme = theme
                request.user.profile.save()

            return Response({'message':"Theme selected successfully!"},status=status.HTTP_202_ACCEPTED)


class File(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        path = request.GET.get("path")

        with open(request.GET.get("path"), 'r') as file:
            content = file.read()

            file = {'name': os.path.basename(
                path), 'path': path, 'is_folder': os.path.isdir(path), 'content': content}

            return Response(file)

    def post(self, request, *args, **kwargs):
        path = os.path.join(request.GET.get("path"), request.data.get("file"))

        with open(path, 'w') as file:
            file.write('')

        with open(path, 'r') as file:
            code = get_object_or_404(Code, pk=request.GET.get('id'))

            explorer = {'name': os.path.basename(
                path), 'path': path, "content": file.read(), 'is_folder': False}

            code = display_tree(code.path)

            return Response({'code': code, 'explorer': explorer})

    def put(self, request, *args, **kwargs):
        print(" Put Request Data ", request.GET)

        code = get_object_or_404(Code, pk=request.GET.get('id'))

        with open(request.data.get("path"), 'w') as file:
            file.write(request.data.get("content"))

        folder = display_tree(code.path)
        return Response(folder)

    def delete(self, request, *args, **kwargs):
        try:
            code = get_object_or_404(Code, pk=request.GET.get('id'))

            os.remove(request.GET.get("path"))
            folder = display_tree(code.path)
            return Response(folder)
        except OSError as e:
            raise Exception(f"Error deleting the file: {e}")


class Folder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        code = get_object_or_404(Code, pk=request.GET.get("id"))

        path = os.path.join(request.GET.get("path"),
                            request.data.get("folder"))

        try:
            os.mkdir(path)
            folder = display_tree(code.path)
            return Response(folder)
        except OSError as e:
            raise Exception(f"Error creating the folder: {e}")

    def delete(self, request, *args, **kwargs):
        try:
            code = get_object_or_404(Code, pk=request.GET.get("id"))

            print(" Path ", request.GET.get("path"))

            shutil.rmtree(request.GET.get("path"))
            folder = display_tree(code.path)
            return Response(folder)
        except OSError as e:
            raise Exception(f"Error deleting the file: {e}")


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(request.user)

        return Response(serializer.data)


class CodeDirectoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = CodeDirectorySerializer(
            request.user.profile.codes.filter(is_active=True), many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Code, pk=request.data.get('id'))

        with transaction.atomic():
            path = os.path.join(get_templates_directory(),
                                request.user.username)

            directories = os.listdir(path)

            name = request.data.get('name') + str(len([directory for directory in directories if request.data.get(
                'name') in directory])) if request.data.get('name') in directories else request.data.get('name')

            data = {
                'user': request.user.profile.id,
                "name": name,
                'path': os.path.join(path, name),
                'image': instance.image
            }

            serializer = CodeDirectorySerializer(data=data)

            if serializer.is_valid():
                template_directory = os.path.join(os.path.join(
                    get_templates_directory(), request.user.username), name)

                shutil.copytree(instance.path, template_directory)

                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThemePublishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        production_code = get_object_or_404(Code, pk=request.data.get('id'))

        live_code = get_object_or_404(Code, public=True)

        base_name = os.path.basename(live_code.path)

        template_directory = os.path.join(
            get_templates_directory(), request.user.username)

        if base_name in os.listdir(template_directory):
            shutil.rmtree(live_code.path)

        shutil.copytree(production_code.path, live_code.path)

        production_code.is_active = False

        production_code.save()
        live_code.save()

        return Response({"message": "Published Successfully"}, status=status.HTTP_202_ACCEPTED)
