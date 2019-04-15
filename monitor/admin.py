from django.contrib import admin
from monitor import models
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class HostAdmin(admin.ModelAdmin):
    list_display = ('id','hostname','ip_address','status')
    filter_horizontal = ('host_groups','templates')

class TemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('service','triggers')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name','interval','plugin_name')

class ActionsAdmin(admin.ModelAdmin):
    list_display = ('name','triggers','hosts','interval','operation')

class ActionOperationAdmin(admin.ModelAdmin):
    list_display = ('name','step','action_type')

class StrategyAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'service', 'service_index', 'specificed_index_key', 'operator_type','data_calculator_func','threshold','logic_type')

class StrategyInline(admin.TabularInline):
    model = models.Strategy


class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name','trigger_level','enable')
    inlines = [StrategyInline]

admin.site.register(models.Host,HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.Template)
admin.site.register(models.ServiceIndex)
admin.site.register(models.Services,ServicesAdmin)
admin.site.register(models.Userprofile)
admin.site.register(models.Actions)
admin.site.register(models.ActionOperation)
admin.site.register(models.Trigger,TriggerAdmin)
admin.site.register(models.Strategy,StrategyAdmin)
