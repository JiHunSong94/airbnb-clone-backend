from rest_framework.serializers import ModelSerializer
from categories.serializers import CategorySerializer

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
    category = CategorySerializer()
    perks = PerkSerializer(many=True)

    class Meta:
        model = Experience
        fields = "__all__"
