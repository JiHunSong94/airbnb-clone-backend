from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied

from reviews.serializers import ReviewSerializer

from .models import Experience, Perk
from .serializers import (
    ExperienceDetailSerializer,
    ExperienceSerializer,
    PerkSerializer,
)
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateExperienceSerializer


class Experiences(APIView):
    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(all_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            experience = serializer.save(host=request.user)
            return Response(ExperienceSerializer(experience).data)
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_experience = serializer.save()
            return Response(ExperienceDetailSerializer(updated_experience).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = PerkSerializer(experience.perks.all(), many=True)
        return Response(serializer.data)


class ExperienceReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page
        end = start + page_size
        experience = self.get_object(pk)
        serializer = ReviewSerializer(
            experience.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                experience=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                user=request.user,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, reqeust, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.user != request.user:
            raise PermissionDenied
        serializer = PublicBookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_booking = serializer.save()
            serializer = PublicBookingSerializer(updated_booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.user != request.user:
            raise PermissionDenied
        booking.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(PerkSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        perk = self.get_objects(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
