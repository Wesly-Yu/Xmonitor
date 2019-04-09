#coding=utf-8
from django.shortcuts import render,HttpResponse

from Xmonitor import settings
from monitor.get_api_data import Client_operation
import json
from django.views.decorators.csrf import csrf_exempt
from monitor.redis_con import redis_conn




REDIS_OBJ = redis_conn.redis_conn(settings)

def client_config(request,client_id):
    config_obj = Client_operation(client_id)
    config = config_obj.get_configs()
    if config:
        return HttpResponse(json.dumps(config))

@csrf_exempt
def service_report(request):
    print('client_data:',request.POST)
    return  HttpResponse(json.dumps("received service data"))