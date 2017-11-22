import json
from django.shortcuts import render_to_response
from django.shortcuts import render 
from django.http import HttpRequest, HttpResponse

def index(request):
    """
    Params:
    	HttpRequest: from django.http
    Returns:
	HttpResponse: with the rendered text of the specified file
    """
    return render(request, 'index.html')
