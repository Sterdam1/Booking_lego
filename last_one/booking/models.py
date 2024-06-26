from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FieldChoise(models.Model):
    choise = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.choise
    
class NewField(models.Model):
    field_name = models.CharField(max_length=100, verbose_name="Название поля", help_text="Введите название поля, которое будет в таблице")
    choise = models.ManyToManyField(FieldChoise)
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

# Comment: Возможно надо будет удалить
# Модель для того чтобы узнать кто что бронировал 
class BookingInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    event = models.CharField(max_length=100)
    book_id = models.IntegerField()

    def __str__(self):
        return self.user + ' booked someting in ' + self.event
    

