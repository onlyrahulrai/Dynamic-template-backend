from django.urls import path
from .views import *

urlpatterns = [ 
    path("user-details/",UserDetails.as_view(),name="user-details"),
    path("code/",Home.as_view(),name="code"),
    path("file/",File.as_view(),name="file"),
    path("folder/",Folder.as_view(),name="folder"),
]