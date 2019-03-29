from django.contrib import admin
from monitor import models
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class HostAdmin(admin.ModelAdmin):
    list_display = ('id','hostname','ip_address','status')
    filter_horizontal = ('host_groups','templates')

class TemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('service')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name','interval','plugin_name')






admin.site.register(models.Host,HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.Template)
admin.site.register(models.ServiceIndex)
admin.site.register(models.Services,ServicesAdmin)
admin.site.register(models.Userprofile)