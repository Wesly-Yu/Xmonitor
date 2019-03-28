from django.db import models



'''监控的主机--服务器端'''
class Host(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    host_group = models.ManyToManyField('HostGroup',blank=True)
    agent_choices = (('snmp','snmp'),('agent','agent'),('wget','wget'))
    agent_type = models.SmallIntegerField(agent_choices)
    templates = models.ManyToManyField("Template",blank=True)
    status_choices = ((0,'Offline'),(1,'Online'),(2,'Error'),(3,'Down'),(4,'Unreachable'))
    status = models.SmallIntegerField(status_choices,default=0)
    enable = models.BooleanField(default=True)
    desc = models.TextField(u"备注",blank=True,null=True)
    host_alive_check_interval = models.IntegerField(u"检查主机存活间隔",default=30)
    def __str__(self):
        return self.hostname


'''存储监控服务指标(比如cpu  memery I/O等)'''
class Services(models.Model):
    service_name = models.CharField(max_length=64)
    indexs = models.ManyToManyField("ServiceIndex",blank=True,verbose_name=u'指标列表')
    interval = models.PositiveIntegerField(default=60,verbose_name='监控间隔')
    plugin_name = models.CharField(u'插件名',max_length=64)
    sub_items = models.BooleanField(default=False,help_text=u'如果一个服务还有独立的子服务，选择这个')
    memo = models.TextField(u'备注', blank=True, null=True)
    def __str__(self):
        return self.service_name


'''存储监控服务指标数据（比如cpu的指标 idle IO wait等等）'''
class ServiceIndex(models.Model):
    index_name = models.CharField(max_length=64,unique=True)    #指标名称
    real_key =models.CharField(max_length=64) #真正关注的指标
    data_type_choices = (('int','int'),('str','str'),('float','float'))
    data_type = models.PositiveIntegerField(u'数据指标类型',choices=data_type_choices,default=0)
    def __str__(self):
        return self.index_name


'''监控模板'''
class Template(models.Model):
    template_name = models.CharField(max_length=64,unique=True)
    service = models.ManyToManyField("Services",blank=True)
    def __str__(self):
        return self.template_name



'''主机组--方便监听多个主机'''
class HostGroup(models.Model):
    group_name = models.CharField(max_length=64,unique=True)
    templates = models.ManyToManyField("Template",blank=True)
    memo = models.TextField(u'备注',blank=True,null=True)
    def __str__(self):
        return self.group_name