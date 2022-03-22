from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    auth = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.name