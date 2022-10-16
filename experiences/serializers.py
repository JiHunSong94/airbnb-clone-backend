from rest_framework.serializers import ModelSerializer

from users.serializers import TinyUserSerializer
from .models import Experience, Perk


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "price",
            "address",
            "start",
            "end",
        )


class ExperienceDetailSerializer(ModelSerializer):

    host = TinyUserSerializer()
    perks = PerkSerializer(many=True)

    class Meta:
        model = Experience
        exclude = ("category",)
