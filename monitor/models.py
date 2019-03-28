from django.db import models



'''监控的主机--服务器端'''
class Host(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    agent_choices = ((0,'snmp'),(1,'agent'))
    agent_type = models.SmallIntegerField(agent_choices)
    templates = models.ManyToManyField("Templates",blank=True)
    status_choices = ((0,'Unknow'),(1,'Ok'),(2,'Error'),(3,'Down'))
    status = models.SmallIntegerField(status_choices,default=0)
    enable = models.BooleanField(default=True)


'''存储监控服务数据'''
class Services(models.Model):
    pass

class Templates(models.Model):
    pass