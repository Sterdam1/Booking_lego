from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewField(models.Model):
    field_name = models.CharField(max_length=100, verbose_name="Название поля", help_text="Введите название поля, которое будет в таблице")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.field_name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)    
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username
