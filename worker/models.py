from operator import mod
from django.db import models
from accounts.models import User
from user.models import Job

# Create your models here.

class ApplyJob(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    applied = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    applied_date = models.DateTimeField(auto_now_add=True,null=True)