
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
       path('api-auth/', include('rest_framework.urls')),
       path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
       # Optional UI:
       path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
       path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
       path('api/v1/',include('apps.urls')),

]
