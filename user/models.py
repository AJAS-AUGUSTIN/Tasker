from operator import mod
from telnetlib import STATUS
from django.db import models
from admin.models import Categories
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    minimum_wage = models.IntegerField()
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    landmark = models.CharField(max_length=100)
    requirements = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    review = models.BooleanField(default=False)
    worker = models.ForeignKey(User, related_name='worker',null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class ReviewRating(models.Model):

    title = models.CharField(max_length=100)
    review = models.CharField(max_length=500)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_id', null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    