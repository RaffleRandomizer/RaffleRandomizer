from randomizer.models import BotAddedToPlace
from telegram.models import TelegramUser


async def get_place(place_id: str):
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(place_id=place_id).afirst()
    return place

async def get_place_by_pk(place_pk: str) -> BotAddedToPlace:
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(pk=place_pk).afirst()
    return place

async def get_place_by_channel_name(channel_username: str) -> BotAddedToPlace:
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(channel_username=channel_username).afirst()
    return place



async def create_place(title: str, place_type: str, place_id: str, admin_rights: bool, username:str|None):
    place = await BotAddedToPlace.objects.acreate(
        title=title,
        place_type=place_type,
        place_id=place_id,
        admin_rights=admin_rights,
        channel_username=username,
    )
    return place

async def update_place_admins(place_id: str, admins_list: list[TelegramUser]):
    print("call_admin_list update")
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(place_id=place_id).afirst()
    if place:
        if place.admin_or_owner.filter(pk=admins_list[0].pk).exists():
            return False
        await place.admin_or_owner.aadd(*admins_list)
        print("admin_list updated")
    return place

async def update_place_id(place_id: str, new_id: str):
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(place_id=place_id).afirst()
    if place:
        place.place_id = new_id
        await place.asave()
    return place

async def update_place_type_and_title(place_id: str, title:str, place_type:str, username:str|None):
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(place_id=place_id).afirst()
    if place:
        place.title = title
        place.place_type = place_type
        place.channel_username = username
        await place.asave()
    return place


async def update_place_admin_rights(place_id: str, admin_rights: bool):
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(place_id=place_id).afirst()
    if place:
        place.admin_rights = admin_rights
        await place.asave()
    return place


async def delete_place(place_id: str):
    place: BotAddedToPlace = await BotAddedToPlace.objects.filter(place_id=place_id).afirst()
    deleted = False
    if place:
        await place.adelete()
        deleted = True
    return deleted

async def delete_admin_from_place(place: BotAddedToPlace, user: TelegramUser):
    if not place.admin_or_owner.filter(pk=user.pk).exists():
        return False
    place.admin_or_owner.remove(user)
    return True


