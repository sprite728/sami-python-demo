from django.template import RequestContext
from django.shortcuts import render_to_response

#Displays the home page

def home(request):
    context = RequestContext(request)
    context_dict = {'active': "home"}
    return render_to_response('index.html', context_dict, context)
