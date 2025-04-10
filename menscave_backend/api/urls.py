from django.urls import path
from .views import WorkshopListCreateAPIView, WorkshopRetrieveUpdateDestroyAPIView, ReservationListCreateAPIView, ReservationRetrieveUpdateDestroyAPIView, ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView
from .views import MessageListCreateAPIView, MessageRetrieveUpdateDestroyAPIView, WorkshopImageCreateAPIView,RegisterUserAPIView,ProfileRetrieveUpdateAPIView
from .views import AvailabilityListCreateAPIView, UserDetailAPIView

urlpatterns = [
  
  
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('profile/', ProfileRetrieveUpdateAPIView.as_view(), name='profile'),
    # Workshop endpoints:
    path('workshops/', WorkshopListCreateAPIView.as_view(), name='workshop-list-create'),
    path('workshops/<int:pk>/', WorkshopRetrieveUpdateDestroyAPIView.as_view(), name='workshop-detail'),

    # Reservation endpoints:
    path('reservations/', ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationRetrieveUpdateDestroyAPIView.as_view(), name='reservation-detail'),
    path('api/availability/workshop/<int:workshop_id>/', AvailabilityListCreateAPIView.as_view(), name='availability'),

      # Oceny i komentarze
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),

    # Messages
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyAPIView.as_view(), name='message-detail'),

    path('workshops/<int:pk>/upload-image/', WorkshopImageCreateAPIView.as_view(), name='workshop-upload-image'),

]