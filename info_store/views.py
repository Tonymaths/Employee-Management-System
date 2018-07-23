from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


# disabling csrf (cross site request forgery)
@csrf_exempt
def index(request):
    if request.method == 'POST':
        # getting values from post
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_number=request.POST.get('number')
        contact=request.POST.get('contact')
        # adding the values in a context variable
        context = {
            'name': name,
            'email': email,
            'number': phone_number,
            'contact': contact,
        }

        # getting our showdata template
        template = loader.get_template('result.html')

        # returing the template
        return HttpResponse(template.render(context, request))
    else:
        # if post request is not true
        # returing the form template
        template = loader.get_template('index.html')
        return HttpResponse(template.render())