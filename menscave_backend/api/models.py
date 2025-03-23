from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

class Workshop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=7, decimal_places=2)
    equipment = models.TextField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    rental_terms = models.TextField()

class WorkshopImage(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to='workshop_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Availability(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="availability")
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()



class Reservation(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation ({self.renter.username}) - {self.workshop.name}"
    
class Review(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
