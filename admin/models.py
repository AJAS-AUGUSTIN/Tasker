from django.db import models



class Categories(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title
