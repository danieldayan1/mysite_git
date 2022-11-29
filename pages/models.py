from django.urls import reverse
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50 )
    password = models.CharField(max_length=8 , unique=True )
    mail = models.EmailField(null=True)
    tel = models.CharField(max_length=11)
    age = models.IntegerField(null=True)
    url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name 

    def get_absolute_url(self):
         return reverse('Home', args=[self.name])



class Projects(models.Model):
    code = models.IntegerField(unique=True)
    desc = models.CharField(max_length=50)

    def __str__(self):
        return self.desc

    def get_absolute_url(self):
        return reverse('projects.html')