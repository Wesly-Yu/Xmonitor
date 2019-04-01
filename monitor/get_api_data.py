#conding=utf-8
from monitor import models
import json,time
from django.core.exceptions import ObjectDoesNotExist


class Client_operation(object):

    def __init__(self,client_id):
        self.client_id = client_id
        self.client_configs = {
            "services":{}
        }
    def get_configs(self):
       try:
           host_obj = models.Host.objects.get(id=self.client_id)
           template_list = list(host_obj.templates.select_related()) #对主机关联的列表去重
           for host_group in host_obj.host_groups.select_related():
               template_list.extend(host_group.templates.select_related())
               print(template_list)
               for template in  template_list:
                   for service in template.service.select_related():
                       print(service)
                       self.client_configs['services'][service.service_name]=[service.plugin_name,service.interval]
       except ObjectDoesNotExist:
           pass
       return self.client_configs
