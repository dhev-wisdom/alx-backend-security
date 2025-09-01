from django.db import models

# Create your models here.

class RequestLog(models.Model):
    """RequestLog model"""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=200)

    def __str__(self):
        return self.ip_address
