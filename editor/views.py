from django.http import JsonResponse
from .utils import display_tree
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(["GET"])
def home(request):
    folder = display_tree(request.user.username)
    return Response(folder)