from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
    )

    role = models.CharField(max_length=20, choices=ROLES)


class Projects(models.Model):
    projects =  models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.projects

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('inprogress', 'In Progress'),
        ('testing', 'Testing'),
        ('completed', 'Completed'),
    )
    projects =  models.ForeignKey(Projects,null=True,blank=True,on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE,related_name='tasks_assigned_to')
    assigned_by = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE,related_name='tasks_assigned_by')

    def __str__(self):
        return self.name
 
    
