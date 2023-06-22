from django.urls import path
from .views import *

urlpatterns = [ 
    path("",ThemeAPIView.as_view(),name="themes"),
    path("publish/",ThemePublishView.as_view(),name="publish"),
    path("code-directories/",CodeDirectoriesView.as_view(),name="code-directories"),
    path("user-details/",UserDetails.as_view(),name="user-details"),
    path("code/",Home.as_view(),name="code"),
    path("file/",File.as_view(),name="file"),
    path("folder/",Folder.as_view(),name="folder"),
]