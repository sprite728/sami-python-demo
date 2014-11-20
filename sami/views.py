from django.template import RequestContext
from django.shortcuts import render_to_response

#Displays the home page

def home(request):
    context = RequestContext(request)
    contextDict = {'active': "home"}
    return render_to_response('index.html', contextDict, context)
