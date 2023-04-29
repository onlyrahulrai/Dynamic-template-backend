from django.shortcuts import redirect

def decorate_func(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated and request.user.profile.theme:
            return view_func(request,*args,**kwargs)
        return redirect('/theme')
    return wrapper
