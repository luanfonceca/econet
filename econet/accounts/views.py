#!/usr/bin/env python
# encoding: utf-8

from django.template import RequestContext
from django.template.defaultfilters import linebreaks
from django.shortcuts import redirect, render_to_response
from django.contrib import messages, auth
from django.utils import simplejson as json
from django.http import HttpResponse

from accounts.models import User
from accounts.forms import UserForm, LoginForm

def register(request):
    user_form = UserForm(request.POST or None)
    
    if user_form.is_valid():
        user = user_form.save()
        messages.success(request, u'Salvou o novo Usuário.')
        return redirect('home')
    else:
        messages.error(request, u'Deu Error visse')

    data = {
        'form': user_form,
    }
    return render_to_response(
        'registration/registration_form.html',
        data, 
        context_instance=RequestContext(request)
    )

def login(request):
    login_form = LoginForm(data=request.POST or None)

    if request.method == 'POST':
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = auth.authenticate(username=data['username'],
                                     password=data['password'])
            if user and user.is_active:
                auth.login(request, user)
                return redirect(
                    request.GET.get('next', 'home')
                )
        messages.error(request, u'Username ou Senha estão incorretas.')

    template_context = {
        "form": login_form,
    }
    return render_to_response('registration/login.html', template_context,
            context_instance=RequestContext(request))


# @login_required
def logout(request):
    auth.logout(request)
    messages.info(request, u"Obrigado por acessar nosso sistema.")
    return redirect('auth_login')
