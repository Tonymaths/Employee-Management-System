from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import re


# disabling csrf (cross site request forgery)
@csrf_exempt
def index(request):
    if request.method == 'POST':
        # getting values from post
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_number=request.POST.get('number')
        contact=request.POST.get('contact')
        pattern=r'[^@]+@[^@]+\.[^@]+'
        email_pattern=re.match(pattern, email)
        if email_pattern is None:
 # adding the values in a context variable
            context={
            'error':'PLEASE ENTER A VALID EMAIL ADDRESS',
            }
            return render(request,'index.html', context)
        if name=='' or  email=='' or phone_number=='' or contact=='':
            context={
            'error' :'PLEASE ENTER ALL FIELDS'}
            return render(request,'index.html', context)
        else:

          context = {
            'name': name,
            'email': email,
            'number': phone_number,
            'contact': contact,
           }
        return render(request,'result.html', context)
    return render(request,'index.html')
