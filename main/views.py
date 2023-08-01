from django.http import HttpResponse

def real_home(request):
    return HttpResponse('The home page..')