from django.shortcuts import render,get_object_or_404,redirect

def school_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_school:
            print(request.user,"dewiudfqiwudnon")
            print(request.META)
            return redirect('school_name')
        else:
            return function(request, *args, **kwargs)
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap