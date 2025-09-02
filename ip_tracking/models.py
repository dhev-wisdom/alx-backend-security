from django.db import models

# Create your models here.

class RequestLog(models.Model):
    """RequestLog model"""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=200)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.id}"
    

class BlockedIP(models.Model):
    """Blocked IP Model"""
    ip_address = models.GenericIPAddressField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.id}"
