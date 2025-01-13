from bot.utils.date_worker import get_datiteme_object
from randomizer.models import *
from django.core.files import File
from dataclasses import dataclass
from randomizer.services import chat as cs
from datetime import datetime
import os
from telegram.models import TelegramUser


@dataclass
class GiveawayData:
    button_type_text:str
    winners_count:int
    post_giv_dt: datetime
    post_channel_id: str
    giv_text: str = None
    check_sub_channels: tuple = ()
    giv_results_dt: str = None
    giv_results_count: str = None



async def create_giveaway(file_path:str, file_name:str, giv_data:GiveawayData, user:TelegramUser=None):
    obj = Giveaway(
                giv_text=giv_data.giv_text,
                winners_count=giv_data.winners_count,
                button_type_text=giv_data.button_type_text,
                post_giv_dt=giv_data.post_giv_dt,
                giv_results_dt=get_datiteme_object(giv_data.giv_results_dt) if giv_data.giv_results_dt else None,
                giv_results_count=giv_data.giv_results_count,
                creator=user,
            )
    
    if file_path:
        with open(file_path, "rb") as file:
            if file_path.endswith(".jpg"):
                obj.photo.save(
                    file_name,
                    File(file)
                )
            else:
                obj.video.save(
                    file_name,
                    File(file)
                )
    await obj.asave()
    if giv_data.check_sub_channels:
        for channel in giv_data.check_sub_channels:
            if place:=await cs.get_place_by_pk(channel):
                obj.check_sub_channels.add(place)
        
    if place:=await cs.get_place_by_pk(giv_data.post_channel_id):
        obj.post_channels = place
    await obj.asave()
    if file_path:
        os.remove(file_path)
    return obj


async def get_giveaway_by_uuid(giv_uuid:str):
    return await Giveaway.objects.filter(unique_id=giv_uuid).select_related("creator","creator__selected_language", "post_channels").afirst()

def get_giveaway_by_uuid_sync(giv_uuid:str):
    return Giveaway.objects.filter(unique_id=giv_uuid).select_related("creator","creator__selected_language", "post_channels").first()


async def get_giveaway_by_pk(giv_pk:str):
    return await Giveaway.objects.filter(pk=giv_pk).select_related("creator", "creator__selected_language", "post_channels").afirst()

async def get_user_givs(user:TelegramUser):
    givs = []
    async for giv in Giveaway.objects.filter(creator=user, deleted_by_creator=False):
        givs.append(giv)
    return givs

async def get_parts_count(giv_obj:Giveaway):
    giv_pk = giv_obj.pk
    giv: Giveaway = await Giveaway.objects.filter(pk=giv_pk).prefetch_related("parts").afirst()
    parts_count = await giv.parts.acount()
    return parts_count

async def get_parts(giv_obj:Giveaway):
    giv_pk = giv_obj.pk
    giv: Giveaway = await Giveaway.objects.filter(pk=giv_pk).prefetch_related("parts").afirst()
    parts = []
    async for particiant in giv.parts.filter():
        parts.append(particiant)
    return parts


async def update_giv_photo_id(giv_obj:Giveaway, photo_id:str):
    giv_obj.photo_id = photo_id
    await giv_obj.asave()


async def update_giv_video_id(giv_obj:Giveaway, video_id:str):
    giv_obj.video_id = video_id 
    await giv_obj.asave()

async def update_giv_end_dt(giv_obj:Giveaway, date: datetime):
    giv_obj.giv_results_count = None
    giv_obj.giv_results_dt = date
    await giv_obj.asave()

async def update_giv_end_count(giv_obj:Giveaway, count):
    giv_obj.giv_results_count = count
    giv_obj.giv_results_dt = None
    await giv_obj.asave()

async def update_giv_deleted(giv_obj:Giveaway):
    giv_obj.deleted_by_creator = True
    await giv_obj.asave()

async def update_giv_ended(giv_obj:Giveaway):
    await Giveaway.objects.filter(pk=giv_obj.pk).aupdate(ended=True)


async def update_giv_ended_by_creator(giv_obj:Giveaway):
    giv_obj.ended_by_creator = True
    await giv_obj.asave()

async def create_giv_post(place_id:str|int, giv_obj:Giveaway, mes_id:str, mes_link:str):
    place = await cs.get_place(place_id=place_id)
    giv_post = GiveawayPostMessage(
        channel=place,
        giveaway=giv_obj,
        message_id=mes_id,
        message_link=mes_link,
    )
    await giv_post.asave()
    return giv_post

async def get_giv_post_by_place_and_giveaway(place: BotAddedToPlace, giveaway: Giveaway):
    return await GiveawayPostMessage.objects.filter(channel=place, giveaway=giveaway).afirst()

async def create_giveaway_part(name:str, telegram_id:str|int, bot_blocked:bool=False, username:str=None):
    giv_part = GivParticipant(
        name=name,
        telegram_id=telegram_id,
        bot_blocked=bot_blocked,
        username=username,
    )
    await giv_part.asave()
    return giv_part

async def add_new_giv_to_part(giv_part:GivParticipant, giv_obj:Giveaway):
    await giv_part.giveaway.aadd(giv_obj)
    


async def get_giveaway_part(telegram_id:str|int):
    return await GivParticipant.objects.filter(telegram_id=telegram_id).afirst()
    
async def get_giv_participant_givs(telegram_id:str|int):
    giv_part = await GivParticipant.objects.filter(telegram_id=telegram_id).afirst()
    givs_list = []
    async for giv in giv_part.giveaway.filter():
        givs_list.append(giv)
    return givs_list




def get_givs_from_two_mins_till_now(two_mins: datetime, now:datetime):
    return Giveaway.objects.filter(post_giv_dt__range=(two_mins, now), ended=False, deleted_by_creator=False, ended_by_creator=False).prefetch_related("posts").all()


def get_givs_from_two_mins_till_now_ended(two_mins: datetime, now:datetime):
    return Giveaway.objects.filter(giv_results_dt__lt=now, ended=False, deleted_by_creator=False, ended_by_creator=False).prefetch_related("posts").all()


async def create_giv_winner(place:int, participant:GivParticipant, giv_obj:Giveaway):
    giv_winner = GiveawayWinners(
        place=place,
        winner=participant,
        giveaway=giv_obj,
    )
    await giv_winner.asave()
    return giv_winner

async def get_giv_winners(giv_obj:Giveaway):
    giv_pk = giv_obj.pk
    giv: Giveaway = await Giveaway.objects.filter(pk=giv_pk).prefetch_related("winners", "winners__winner").afirst()
    winners = []
    async for winner in giv.winners.order_by("place").select_related("winner").filter():
        winners.append(winner)
    return winners


async def get_giv_check_channels(giv:Giveaway):
    giv_pk = giv.pk
    giv: Giveaway = await Giveaway.objects.filter(pk=giv_pk).prefetch_related("check_sub_channels").afirst()
    channels = []
    async for channel in giv.check_sub_channels.filter():
        channels.append(channel.place_id)
    return channels

async def get_price(lines_count:int):
    price_obj = await Price.objects.filter(lt_count__gte=lines_count).order_by("lt_count").afirst()
    return price_obj.price
