import os
import shutil
from .utils import display_tree
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailSerializer

# Create your views here.
class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        folder = display_tree(request.user.username)
        return Response(folder)

class File(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        path = request.GET.get("path")

        with open(request.GET.get("path"), 'r') as file:
            content = file.read()

            file = {'name':os.path.basename(path),'path':path,'is_folder':os.path.isdir(path),'content':content}

            return Response(file)

    def post(self, request, *args, **kwargs):
        path = os.path.join(request.GET.get("path"), request.data.get("file"))

        with open(path, 'w') as file:
            file.write('')

        folder = display_tree(request.user.username)
        return Response(folder)

    def put(self, request, *args, **kwargs):
        with open(request.data.get("path"), 'w') as file:
            file.write(request.data.get("content"))

        folder = display_tree(request.user.username)
        return Response(folder)

    def delete(self, request, *args, **kwargs):
        try:
            os.remove(request.GET.get("path"))
            folder = display_tree(request.user.username)
            return Response(folder)
        except OSError as e:
            raise Exception(f"Error deleting the file: {e}")

class Folder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        path = os.path.join(request.GET.get("path"),
                            request.data.get("folder"))
        try:
            os.mkdir(path)
            folder = display_tree(request.user.username)
            return Response(folder)
        except OSError as e:
            raise Exception(f"Error creating the folder: {e}")

    def delete(self, request, *args, **kwargs):
        try:
            shutil.rmtree(request.GET.get("path"))
            folder = display_tree(request.user.username)
            return Response(folder)
        except OSError as e:
            raise Exception(f"Error deleting the file: {e}")

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)