from rest_framework.serializers import ModelSerializer
from .models import Experience, Perk


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "name",
            "price",
            "address",
            "start",
            "end",
        )
