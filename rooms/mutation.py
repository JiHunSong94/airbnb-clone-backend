import enum
import typing
from django.db import transaction
import strawberry
from strawberry.types import Info
from enum import Enum
from .models import Room, Amenity
from categories.models import Category


@strawberry.enum
class RoomKindChoices(Enum):
    ENTIRE_PLACE = "entire_place"
    PRIVATE_ROOM = "private_room"
    SHARED_ROOM = "shared_room"


def add_room(
    info: Info,
    category_pk: int,
    name: str,
    country: str,
    city: str,
    price: int,
    rooms: int,
    toilets: int,
    description: str,
    address: str,
    pet_friendly: bool,
    kind: RoomKindChoices,
    amenities: typing.List[int],
):
    try:
        category = Category.objects.get(pk=category_pk)
        if category.kind == Category.CategoryKindChoices.EXPERIENCES:
            raise Exception("The category kind should be 'rooms'")
    except Category.DoesNotExist:
        raise Exception("Category not found")
    try:
        with transaction.atomic():
            room = Room.objects.create(
                name=name,
                country=country,
                city=city,
                price=price,
                rooms=rooms,
                toilets=toilets,
                description=description,
                address=address,
                pet_friendly=pet_friendly,
                kind=kind.value,
                owner=info.context.request.user,
                category=category,
            )
            for amenity_pk in amenities:
                amenity = Amenity.objects.get(pk=amenity_pk)
                room.amenities.add(amenity)
            room.save()
            print(kind.value)
            return room
    except Exception:
        raise Exception("Amenity not found")
