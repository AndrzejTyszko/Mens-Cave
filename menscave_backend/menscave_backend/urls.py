from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from api.views import AvailabilityListCreateAPIView
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # dodaj tę linię
    path("admin/", staff_member_required(admin.site.urls)),  # Tylko dla staff!


    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('workshops/<int:pk>/availability/', AvailabilityListCreateAPIView.as_view(), name='workshop-availability'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

