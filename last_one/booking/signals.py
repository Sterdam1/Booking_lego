from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import NewField

@receiver(pre_save, sender=NewField)
def check_model_limit(sender, instance, **kwargs):
    current_user_count = NewField.objects.filter(created_by=instance.created_by).count()
    if current_user_count >= 10:
        raise ValidationError("Вы уже создали максимальное количество экземпляров модели")