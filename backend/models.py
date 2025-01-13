from django.db import models

class TimeBasedModel(models.Model):
    class Meta:
        abstract = True
        
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
