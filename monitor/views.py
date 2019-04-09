#coding=utf-8
from django.shortcuts import render,HttpResponse
from monitor.get_api_data import Client_operation
import json

def client_config(request,client_id):
    config_obj = Client_operation(client_id)
    config = config_obj.get_configs()
    if config:
        return HttpResponse(json.dumps(config))


def service_report(request):
    print("ok")
    return  HttpResponse('status:200')