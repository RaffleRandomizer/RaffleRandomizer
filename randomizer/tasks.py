
import asyncio
from typing import List
from randomizer_bot import celery_app
from bot.utils.notifications import send_notification as notifyer
from celery import shared_task
import logging
from datetime import datetime, timedelta
from bot.config.loader import moscow_tz
from randomizer.services import givs as gs
from bot.utils import giv as giv_sender


async def send_givs(givs: List[dict]):
    for giv in givs:
        await giv_sender.send_giv_post_to_place_id_by_giv_pk(**giv)



@celery_app.task
def send_givs_task(givs: List[dict]):
    asyncio.run(send_givs(givs=givs))


@celery_app.task
def send_notification(telegram_id:str|int, text:str):
    asyncio.run(notifyer(telegram_ids=[telegram_id], text=text))


@shared_task
def post_givs():
    logging.info("post_givs started") 
    now = datetime.now().astimezone(moscow_tz)
    two_min_ago = (now - timedelta(minutes=2)).astimezone(moscow_tz)
    givs = gs.get_givs_from_two_mins_till_now(two_mins=two_min_ago, now=now)
    givs_to_post = []
    for giv in givs:
        post_channel = giv.post_channels
        post_exists = giv.posts.filter(channel=post_channel).exists()
        if not post_exists:
            givs_to_post.append({
                "giv_pk": giv.pk,
                "place_id": post_channel.place_id
            })
    send_givs_task.delay(givs=givs_to_post)

    
