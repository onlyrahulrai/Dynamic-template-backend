from django.shortcuts import redirect

def decorate_func(view_func):
    def wrapper(request,*args,**kwargs):
        if (request.user.is_authenticated and request.user.profile.theme) or (request.GET.get('user') and request.GET.get('path')):
            return view_func(request,*args,**kwargs)
        return redirect('/theme')
    return wrapper
