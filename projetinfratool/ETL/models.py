from django.db import models

# Create your models here.


class ecs(models.Model):
    InstanceName =  models.CharField(max_length=255)
    HostName = models.CharField(max_length=255)
    PrimaryIpAddress = models.CharField(max_length=255)
    OSName = models.CharField(max_length=255)
    InstanceTypeFamily = models.CharField(max_length=255)
    Cpu = models.IntegerField()
    Memory = models.IntegerField()
    Status = models.CharField(max_length=255)
    InstanceBandwidthRx = models.IntegerField()
    VSwitchID = models.CharField(max_length=255)
    SecurityGroupId = models.TextField()
    Lastseen = models.DateTimeField()

    class Meta:
        verbose_name =('Ecs')
        verbose_name_plural =('Ecs')
    
    def __str__(self):
        return self.InstanceName

class slb(models.Model):
    SLBName =  models.CharField(max_length=255)
    SLBId = models.CharField(max_length=255)
    SLBIp = models.CharField(max_length=255)
    SLBPort = models.IntegerField()
    SLBEnvironment = models.CharField(max_length=255)
    SLBProtocol = models.CharField(max_length=255)
    SLBNetworkType = models.CharField(max_length=255)
    SLBAlgorithm = models.CharField(max_length=255)
    SLBStatus = models.CharField(max_length=255)
    Lastseen = models.DateTimeField()

    class Meta:
        verbose_name =('Slb')
        verbose_name_plural =('Slb')
    
    def __str__(self):
        return self.SLBName

class rds(models.Model):
    RDSId = models.CharField(max_length=255)
    RDSIp = models.CharField(max_length=255)
    RDSPort = models.IntegerField()
    RDSCpu = models.IntegerField()
    RDSMemory = models.IntegerField()
    RDSIOPS = models.IntegerField()
    RDSMaxConnection = models.IntegerField()
    RDSEngine = models.CharField(max_length=255)
    RDSInstanceType = models.CharField(max_length=255)
    RDSVSwitch = models.CharField(max_length=255)
    RDSStatus = models.CharField(max_length=255)
    RDSFlorian = models.IntegerField()

    class Meta:
        verbose_name =('Rds')
        verbose_name_plural =('Rds')
    
    def __str__(self):
        return self.RDSId
