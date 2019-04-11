#coding=utf-8
from django.shortcuts import HttpResponse

from Xmonitor import settings
from monitor.get_api_data import Client_operation
import json
from django.views.decorators.csrf import csrf_exempt
from monitor.back import redis_con
from monitor.back.redis_data_handle import DataStore


'''{"services": {"LinuxCpu": ["LinuxCpuPlugin", 60], "LinuxLoad": ["LinuxLoadPlugin", 60], "LinuxMemery": ["LinuxMemeryPlugin", 60], "Mysql": ["mysql", 60]}}'''

REDIS_OBJ = redis_con.redis_conn(settings)
# print(REDIS_OBJ.set('new',123))

def client_config(request,client_id):
    config_obj = Client_operation(client_id)
    config = config_obj.get_configs()
    if config:
        return HttpResponse(json.dumps(config))

@csrf_exempt
def service_report(request):
    if request.method == 'POST':
        try:
            print('host=%s,service=%s' %(request.POST.get('client_id'),request.POST.get('service_name')))
            post_data = json.loads(request.POST['data'])
            client_id = request.POST.get('client_id')
            service_name = request.POST.get('service_name')
            data_optimized_save = DataStore(client_id,service_name,post_data,REDIS_OBJ)

        except IndexError as e:
            print('fail',e)

    return  HttpResponse(json.dumps("received service data"))