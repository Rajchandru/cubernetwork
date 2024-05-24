import uuid
from django.db import models

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.CharField(unique=True, max_length=100)
    account_name = models.CharField(max_length=100)
    app_secret_token = models.CharField(max_length=100, unique=True,blank=True)
    website = models.URLField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.app_secret_token:
            self.app_secret_token = uuid.uuid4().hex  # Generate a random token if not provided
        super().save(*args, **kwargs)
        
class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=10)
    headers = models.JSONField(null=True)