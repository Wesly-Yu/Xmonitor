#coding=utf-8
from django.shortcuts import HttpResponse

from Xmonitor import settings
from monitor.get_api_data import Client_operation
import json
from django.views.decorators.csrf import csrf_exempt
from monitor.back import redis_con



'''{"services": {"LinuxCpu": ["LinuxCpuPlugin", 60], "LinuxLoad": ["LinuxLoadPlugin", 60], "LinuxMemery": ["LinuxMemeryPlugin", 60], "Mysql": ["mysql", 60]}}'''

REDIS_OBJ = redis_con.redis_conn(settings)
print(REDIS_OBJ)

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


        except Exception as e:
            print('fail')

    return  HttpResponse(json.dumps("received service data"))