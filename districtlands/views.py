from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@csrf_exempt
def start(request):
    try:
	
        return JsonResponse({'detail' : 'Districts created.', 'districts' : {}}, content_type="application/json", status=200)
    except Exception as e:
    	return JsonResponse({'detail' : 'Failed to start predetermined algorithm', 'error' : str(e)}, content_type="application/json", status=400)




@api_view(['POST'])
@csrf_exempt
def user_start(request):
    try:
    	return JsonResponse({'detail' : 'Districts created.', 'districts' : {}}, content_type="application/json", status=200)
    except Exception as e:
    	return JsonResponse({'detail' : 'Failed to start user algorithm', 'error' : str(e)}, content_type="application/json", status=400)

