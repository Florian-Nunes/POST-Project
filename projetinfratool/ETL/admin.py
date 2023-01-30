from django.contrib import admin
from .models import ecs, slb, rds

# Register your models here.S

class AdminEcsInfo(admin.ModelAdmin):
    list_display = ('InstanceName', 'HostName', 'PrimaryIpAddress', 'OSName', 'InstanceTypeFamily', 'Cpu', 'Memory', 'Status', 'InstanceBandwidthRx', 'VSwitchID', 'SecurityGroupId', 'Lastseen')
admin.site.register(ecs, AdminEcsInfo)

class AdminSlbInfo(admin.ModelAdmin):    
    list_display = ('SLBName', 'SLBId', 'SLBIp', 'SLBPort', 'SLBEnvironment', 'SLBProtocol', 'SLBNetworkType', 'SLBAlgorithm', 'SLBAlgorithm', 'SLBStatus', 'Lastseen')
admin.site.register(slb, AdminSlbInfo)

class AdminRdsInfo(admin.ModelAdmin):
    list_display = ('RDSId', 'RDSIp', 'RDSPort', 'RDSCpu', 'RDSMemory', 'RDSIOPS', 'RDSMaxConnection', 'RDSEngine', 'RDSInstanceType', 'RDSVSwitch', 'RDSStatus')
admin.site.register(rds, AdminRdsInfo) 