from django.db import models
from common.models import CommonModel


class Category(CommonModel):

    """Room or Experience Category"""

    class CategoryKindChioces(models.TextChoices):
        ROOMS = "room", "Room"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=15, choices=CategoryKindChioces.choices)

    def __str__(self) -> str:
        return f"{self.kind}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
