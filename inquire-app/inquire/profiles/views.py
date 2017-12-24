# Create your views here.
import datetime

from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from inquire.profiles.models import UserProfile
from django.http import HttpResponse
from inquire.profiles.forms import MyRegistrationForm
# from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect(reverse('profiles:logout_success'))


def logout_success(request):
    return render_to_response('profiles/logout_success.html')


def profile(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('questions:index'))
    else:
        return HttpResponse("login not successfully")
        return render_to_response('profiles/logout.html',  {})

@csrf_protect
def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('profiles:register_success'))
        
    else:
        form = MyRegistrationForm()
    args = {}
    # args.update(csrf(request))
    
    args['form'] = form
    
    return render(request, 'profiles/register.html', args)



def register_success(request):
    return render_to_response('profiles/register_success.html')
