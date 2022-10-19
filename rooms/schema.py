import strawberry
import typing
from . import types
from . import queries
from . import mutation
from common.permissions import OnlyLoggedIn


@strawberry.type
class Query:
    all_rooms: typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms, permission_classes=[OnlyLoggedIn]
    )
    room: typing.Optional[types.RoomType] = strawberry.field(resolver=queries.get_room)


@strawberry.type
class Mutation:
    room: types.RoomType = strawberry.mutation(
        resolver=mutation.add_room, permission_classes=[OnlyLoggedIn]
    )
