from django.urls import path
from .views import Experiences, Perks, PerkDetail

urlpatterns = [
    path("", Experiences.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
