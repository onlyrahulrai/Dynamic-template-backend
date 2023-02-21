from django.shortcuts import render

# Create your views here.

def home(request):
    print(request.user.templates.first().header_code)
    return render(request,'home.html')