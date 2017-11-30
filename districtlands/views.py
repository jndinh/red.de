from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from .algorithm import districts, tracts


@api_view(['POST', 'GET'])
@csrf_exempt
def start(request):
    '''
    Using a predetermined starting point, send back a list of districts that have been redrawn.
    '''
    #try:
    new_districts = districts._test_redistrict()

    return JsonResponse({'detail' : 'Districts created.', 'districts' : new_districts}, content_type="application/json", status=200)
    #except Exception as e:
    #	return JsonResponse({'detail' : 'Failed to start predetermined algorithm', 'error' : str(e)}, content_type="application/json", status=400)



@api_view(['POST'])
@csrf_exempt
def user_start(request):
    '''
    Using a predetermined starting point, send back a list of districts that have been redrawn.
    '''
    try:
    	return JsonResponse({'detail' : 'Districts created.', 'districts' : {}}, content_type="application/json", status=200)
    except Exception as e:
    	return JsonResponse({'detail' : 'Failed to start user algorithm', 'error' : str(e)}, content_type="application/json", status=400)

