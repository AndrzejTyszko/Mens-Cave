from rest_framework import permissions
from .models import Reservation

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Sprawdzamy, czy użytkownik jest właścicielem rezerwacji (renter), a nie warsztatu (owner)
        if isinstance(obj, Reservation):
            return obj.renter == request.user
        
        # Dla warsztatów i innych obiektów sprawdzamy właściciela
        return obj.owner == request.user

