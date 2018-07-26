from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from.models import Post
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
        num_pattern=re.match(r'[0-9]+', phone_number)

        if name=='' or  email=='' or phone_number=='' or contact=='':
            context={
            'error' :'PLEASE ENTER ALL FIELDS'}
            return render(request,'index.html', context)
        if email_pattern is None:
            # adding the values in a context variable
            context={
                'error':'PLEASE ENTER A VALID EMAIL ADDRESS',
            }
            return render(request,'index.html', context)
        if num_pattern is None:
            context={
                'error':'PLEASE ENTER A VALID PHONE NUMBER',
            }
            return render(request,'index.html', context)
        else:

            p=Post(name=name,email=email, number=phone_number ,contact_address=contact)
            p.save()
            queryset=Post.objects.all()

            context = {
                'all_post': queryset

            }
        return render(request,'result.html', context)
    return render(request,'index.html')
