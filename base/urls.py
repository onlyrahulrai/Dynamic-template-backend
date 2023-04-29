from django.urls import path 
from .views import  *

urlpatterns = [ 
    path("", home,name='home'),
    path("theme/", theme,name='theme'),
    path('select-theme/',select_theme,name="select-theme")
]