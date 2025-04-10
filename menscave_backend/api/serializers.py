from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Workshop, WorkshopImage, Availability, Reservation, Review, Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class WorkshopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopImage
        fields = ['id', 'image']

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

class WorkshopSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    photos = WorkshopImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True) 

    class Meta:
        model = Workshop
        fields = '__all__'


class NestedWorkshopSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Workshop
        fields = ['id', 'name', 'owner']

class ReservationSerializer(serializers.ModelSerializer):
    renter = UserSerializer(read_only=True)
    workshop = NestedWorkshopSerializer(read_only=True)
    workshop_id = serializers.PrimaryKeyRelatedField(
        queryset=Workshop.objects.all(), write_only=True, source='workshop'
    )

    class Meta:
        model = Reservation
        fields = ['id', 'workshop', 'workshop_id', 'renter', 'start_datetime', 'end_datetime', 'total_price', 'created_at']



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'sent_at', 'read_at']
