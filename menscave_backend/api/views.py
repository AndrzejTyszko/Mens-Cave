from rest_framework import generics, permissions, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .models import Workshop, Reservation, Message, Review, Availability, WorkshopImage, User
from django.db import models
from .permissions import IsOwnerOrReadOnly
from decimal import Decimal
from .serializers import ReviewSerializer, MessageSerializer, WorkshopSerializer, ReservationSerializer, WorkshopImageSerializer, WorkshopImageSerializer, AvailabilitySerializer, WorkshopImageSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveAPIView

from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


from rest_framework_simplejwt.views import TokenObtainPairView

class ObtainTokenView(TokenObtainPairView):
    pass  # Możesz dodać własną logikę w przyszłości


@method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True), name="dispatch")
class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

@method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True), name="dispatch")
class ObtainTokenView(TokenObtainPairView):
    pass  # Logowanie JWT



class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully!", "user_id": user.id}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkshopListCreateAPIView(generics.ListCreateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ReservationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(
        models.Q(renter=user) | models.Q(workshop__owner=user)
    )

class ReservationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(
        models.Q(renter=user) | models.Q(workshop__owner=user)
    )


    def perform_create(self, serializer):
        start = serializer.validated_data['start_datetime']
        end = serializer.validated_data['end_datetime']
        now = timezone.now()

        if start < now or end <= start:
            raise serializers.ValidationError("Nieprawidłowy przedział czasowy.")

        workshop = serializer.validated_data['workshop']
        duration_hours = calculate_hours(start, end)
        total_price = workshop.hourly_rate * duration_hours

        serializer.save(renter=self.request.user, total_price=total_price)


def calculate_hours(start, end):
    duration = end - start
    hours = Decimal(duration.total_seconds()) / Decimal(3600)
    return hours.quantize(Decimal('0.01'))  # zaokrąglenie do 2 miejsc po przecinku



class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        workshop_id = self.request.query_params.get('workshop')
        if workshop_id:
            return Review.objects.filter(workshop__id=workshop_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        workshop = serializer.validated_data.get('workshop')
        user = self.request.user

        # ✅ Zabezpieczenie: tylko jedna recenzja na warsztat
        already_exists = Review.objects.filter(workshop=workshop, user=user).exists()
        if already_exists:
            raise serializers.ValidationError("Już wystawiłeś opinię dla tego warsztatu.")

        serializer.save(user=user)

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    

class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user) | Message.objects.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        if 'receiver' not in self.request.data:
            raise serializers.ValidationError({"receiver": "This field is required."})
        serializer.save(sender=self.request.user)
        
class MessageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) | models.Q(receiver=self.request.user)
        )
        
    from rest_framework.parsers import MultiPartParser, FormParser


class WorkshopImageCreateAPIView(generics.CreateAPIView):
    serializer_class = WorkshopImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        workshop_id = self.kwargs.get('pk')
        workshop = Workshop.objects.get(pk=workshop_id)
        serializer.save(workshop=workshop)

class AvailabilityListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Availability.objects.filter(workshop__id=self.kwargs['workshop_id'])

    def perform_create(self, serializer):
        workshop = Workshop.objects.get(pk=self.kwargs['workshop_id'])
        serializer.save(workshop=workshop)


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]