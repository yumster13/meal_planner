from django.shortcuts import redirect


def RedirectView(request,any_url = None):
    if request.user.is_authenticated:
        print(request.user)
        return redirect('home') 
    else: 
        return redirect('login') 