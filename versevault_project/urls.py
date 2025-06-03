from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_root, name='api-root'), # API root view
    path('register/', views.RegisterView.as_view(), name='register'), # User registration view
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Token obtain view 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Token refresh view
    path('profile/', views.ProfileView.as_view(), name='profile'),# User profile view 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
