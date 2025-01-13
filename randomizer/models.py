import asyncio
from typing import List
from celery import shared_task
from django.db import IntegrityError, models
from django.core.exceptions import ValidationError

from backend.models import TimeBasedModel
from telegram.models import TelegramUser
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from bot_data.services import text as ts
from bot.data import bot_data as td
import uuid
import shortuuid
from randomizer_bot import celery_app
from bot.utils.notifications import send_notification as notifyer
from django.contrib import messages



class BotAddedToPlace(TimeBasedModel):
    class Meta:
        verbose_name = 'Куда бот добавлен'
        verbose_name_plural = 'Места куда бот добавлен'
        ordering = ["-created_at"]

    class PlaceType(models.TextChoices):
        GROUP = "group", "Группа (чат)"
        SGROUP = "supergroup", "Супергруппа (чат)"
        CHANNEL = "channel", "Канал"

    title = models.CharField(max_length=255)
    place_type = models.CharField("Тип места", choices=PlaceType.choices)
    admin_or_owner = models.ManyToManyField(TelegramUser, verbose_name="Админ или владелец", related_name="chats", blank=True)
    place_id = models.CharField("ID места в которое добавили бота", max_length=255, unique=True)
    admin_rights = models.BooleanField(default=False)
    channel_username = models.CharField("Юзернейм публичного канала", max_length=512, null=True, blank=True)

    def __str__(self):
        return f"{self.title} | Права админа - {'✅' if self.admin_rights else '❌'}"
    
    @property
    def short_name(self):
        return self.__str__()


class Giveaway(TimeBasedModel):
    class Meta:
        verbose_name = 'Розыгрыш'
        verbose_name_plural = 'Розыгрыши'
        ordering = ["-created_at"]

    unique_id = models.CharField(default=shortuuid.uuid, editable=False, unique=True)
    giv_text = models.TextField("Текст розыгрыша", null=True, blank=True)
    video_id = models.CharField("ID видео", max_length=512, null=True, blank=True)
    video = models.FileField(verbose_name="Видео", upload_to="giv_videos", null=True, blank=True)
    photo = models.FileField(verbose_name="Фото", upload_to="giv_photos", null=True, blank=True)
    photo_id = models.CharField(verbose_name="ID фото", max_length=512, null=True, blank=True)
    button_type_text = models.CharField("Текст кнопки", max_length=128, null=True, blank=True)
    check_sub_channels = models.ManyToManyField(BotAddedToPlace, verbose_name="Проверка подписки на эти каналы", related_name="check_sub_givs", blank=True)
    winners_count = models.IntegerField("Количество победителей", default=1)
    post_channels = models.ForeignKey(BotAddedToPlace, on_delete=models.SET_NULL, verbose_name="Где опубликовать розыгрыш", related_name="givs", blank=True, null=True)
    post_giv_dt = models.DateTimeField("Дата и время публикации", null=True, blank=True)
    giv_results_dt = models.DateTimeField("Дата и время подведения итогов", null=True, blank=True)
    giv_results_count = models.IntegerField("Итоги по количеству участников", null=True, blank=True)
    ended = models.BooleanField("Закончен", default=False)
    creator = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    deleted_by_creator = models.BooleanField("Удален создателем", default=False)
    ended_by_creator = models.BooleanField("Завершен создателем", default=False)

    def __str__(self):
        return f"Розыгрыш {self.pk}"
    
    @property
    def short_name(self):
        return self.__str__()

class GiveawayWinners(TimeBasedModel):
    class Meta:
        verbose_name = 'Победитель розыгрыша'
        verbose_name_plural = 'Победители розыгрыша'
        ordering = ["-created_at"]
        unique_together = (('winner', 'giveaway'), ('place', 'giveaway'))

    place = models.IntegerField("Место")
    winner = models.ForeignKey("GivParticipant", verbose_name="Участник розыгрыша", on_delete=models.CASCADE, related_name="winners")
    giveaway = models.ForeignKey("Giveaway",verbose_name="Розыгрыш", on_delete=models.CASCADE, related_name="winners")


class GiveawayPostMessage(TimeBasedModel):
    class Meta:
        verbose_name = 'Сообщение с розыгрышем'
        verbose_name_plural = 'Сообщения с розыгрышем'
        ordering = ["-created_at"]

    giveaway = models.ForeignKey("Giveaway", on_delete=models.CASCADE, related_name="posts")
    channel = models.ForeignKey(BotAddedToPlace, on_delete=models.SET_NULL, null=True, blank=True, related_name="giv_posts")
    message_id = models.CharField("id поста", max_length=512, null=True, blank=True)
    message_link = models.CharField("Ссылка на сообщение", max_length=512, null=True, blank=True)

    def __str__(self):
        return self.message_link if self.message_link else "-"



class GivParticipant(TimeBasedModel):
    class Meta:
        verbose_name = 'Участник розыгрыша'
        verbose_name_plural = 'Участники розыгрыша'
        ordering = ["-created_at"]
    
    name = models.CharField("ФИО из ТГ", max_length=256)
    telegram_id = models.BigIntegerField("Телеграм ID", unique=True)
    username = models.CharField("Ник Телеграм", max_length=128, null=True, blank=True, default=None)
    bot_blocked = models.BooleanField("Бот заблокирован", default=False)
    giveaway = models.ManyToManyField("Giveaway", blank=True, related_name="parts")

    def __str__(self):
        return f"{self.name} {self.telegram_id}"


class Price(TimeBasedModel):
    class Meta:
        verbose_name = 'Цену на таблицу'
        verbose_name_plural = 'Цены на таблицы'
        ordering = ["lt_count"]
    
    lt_count = models.IntegerField("До скольки строк", null=True, blank=True)
    price = models.IntegerField("Цена", default=10)

    def __str__(self):
        return f"Цена для таблиц до {self.lt_count} строк (включая)- {self.price} ⭐"