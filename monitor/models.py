from django.db import models
from django.contrib.auth.models import User


'''监控的主机--服务器端'''
class Host(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    host_groups = models.ManyToManyField('HostGroup',blank=True)
    monitor_choices = (('snmp','SNMP'),('agent','Agent'),('wget','WGET'))
    monitor_type = models.CharField(u'监控方式',choices=monitor_choices,max_length=64)
    templates = models.ManyToManyField("Template",blank=True)
    status_choices = ((0,'Online'),(1,'Offline'),(2,'Error'),(3,'Down'),(4,'Unreachable'))
    status = models.IntegerField(u'状态',choices=status_choices,default=0)
    desc = models.TextField(u"备注",blank=True,null=True)
    host_alive_check_interval = models.IntegerField(u"检查主机存活间隔",default=30)
    def __str__(self):
        return self.hostname


'''存储监控服务指标(比如cpu  memery I/O等)'''
class Services(models.Model):
    service_name = models.CharField(max_length=64,verbose_name=u'服务名称')
    indexs = models.ManyToManyField("ServiceIndex",blank=True,verbose_name=u'指标列表')
    interval = models.PositiveIntegerField(default=60,verbose_name='监控间隔')
    plugin_name = models.CharField(u'插件名',max_length=64)
    sub_items = models.BooleanField(default=False,help_text=u'如果一个服务还有独立的子服务，选择这个')
    memo = models.TextField(u'备注', blank=True, null=True)
    def __str__(self):
        return self.service_name


'''存储监控服务指标数据（比如cpu的指标 idle IO wait等等）'''
class ServiceIndex(models.Model):
    index_name = models.CharField(max_length=64)    #指标名称
    real_key =models.CharField(max_length=64) #真正关注的指标
    data_type_choices = (('int','int'),('str','str'),('float','float'))
    data_type = models.CharField(u'数据指标类型',choices=data_type_choices,default='int',max_length=64)
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


class Userprofile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=64,blank=True,null=True)
    def __str__(self):
        return self.username




class Strategy(models.Model):
    '''报警策略'''
    trigger = models.ForeignKey('Trigger', verbose_name=u'所属触发器',on_delete=models.CASCADE)
    service = models.ForeignKey('Services', verbose_name=u'关联服务',on_delete=models.CASCADE)
    service_index = models.ForeignKey('ServiceIndex', verbose_name=u'关联服务指标',on_delete=models.CASCADE)
    specificed_index_key = models.CharField(verbose_name=u'只监控专门指定的指标key',max_length=64,blank=True,null=True)
    operator_type_choices = (('equal','='),('lt','>'),('st','<'))             #lt:larger than ,st:small than
    operator_type = models.CharField(u'运算符',choices=operator_type_choices,max_length=32)
    data_calculator_type_choices =(('avg','Average'),
                                   ('max','Max'),
                                   ('hit','Hit'),
                                   ('last','Last'),)
    data_calculator_func = models.CharField(u'数据处理方式',choices=data_calculator_type_choices,max_length=64)
    data_calculator_args = models.CharField(u'函数传入参数',help_text=u'若是多个参数，则用，号分开，第一个值是时间',max_length=64)
    threshold = models.IntegerField(u'阈值')
    logic_type_choices = (('or','OR'),('and','AND'))
    logic_type = models.CharField(u"条件逻辑关系",choices=logic_type_choices,max_length=32,blank=True,null=True)
    def __str__(self):
        return "%s %s(%s(%s))" %(self.service_index,self.operator_type,self.data_calculator_func,self.data_calculator_args)


class Trigger(models.Model):
    '''告警级别'''
    name = models.CharField(u'触发器名称',max_length=64)
    trigger_choices = ((1,'Information')
                      ,(2,'Warning'),
                      (3,'Average'),
                      (4,'High'),
                      (5,'Diaster'))
    trigger_level = models.IntegerField(u'告警级别',choices=trigger_choices)
    enable =models.BooleanField(default=True)
    memo = models.TextField(u'备注',blank=True,null=True)
    def __str__(self):
        return self.name



class Actions(models.Model):
    '''定义触发告警后做什么操作'''
    name = models.CharField(max_length=64)
    triggers = models.ManyToManyField('Trigger',blank=True,help_text=u'触发哪些报警策略')
    hosts = models.ManyToManyField('Host',blank=True)
    interval = models.IntegerField(u'告警间隔(s)',default=300)
    operation = models.ManyToManyField('Actions')
    recover_notice = models.BooleanField(u'故障恢复后发送通知',default=True)
    recover_subject = models.CharField(max_length=128,blank=True,null=True)
    recover_message = models.TextField(blank=True,null=True)
    enable = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class ActionOperation(models.Model):
    '''报警动作'''
    name = models.CharField(max_length=64)
    step = models.SmallIntegerField(u"第n次告警",default=1,help_text="当trigger触发次数小于这个值时就执行这条记录里报警方式")
    action_type_choices = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('script', 'RunScript'),
    )
    action_type = models.CharField(u"动作类型", choices=action_type_choices, default='email', max_length=64)
    notifiers = models.ManyToManyField('Userprofile', verbose_name=u"通知对象", blank=True)
    _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''

    msg_format = models.TextField(u"消息格式", default=_msg_format)

    def __str__(self):
        return self.name