from backend.models import TimeBasedModel
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from bot_data.models import Language


class TelegramUser(TimeBasedModel):
    class Meta:
        verbose_name = "Телеграм Юзер"
        verbose_name_plural = "Телеграм Юзеры"
        ordering = ["-name"]
        
    name = models.CharField("ФИО из ТГ", max_length=256)
    telegram_id = models.BigIntegerField("Телеграм ID", unique=True)
    username = models.CharField("Ник Телеграм", max_length=128, null=True, blank=True, default=None)
    selected_language = models.ForeignKey(Language,on_delete=models.SET_NULL, verbose_name="Выбранный язык", null=True, blank=True, default=None)
    bot_blocked = models.BooleanField("Бот заблокирован", default=False)

    def __str__(self):
        return f"{self.name} {self.telegram_id}"

