from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views
from core.views import CommentView, homepage
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'), # API root view
    path('register/', views.RegisterView.as_view(), name='register'), # User registration view
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Token refresh view
    path('profile/', views.ProfileView.as_view(), name='profile'),# User profile view 
    path('comments/', CommentView.as_view(), name='comments'),  # GET (list), POST (add)
    path('comments/<int:pk>/', CommentView.as_view(), name='comment-detail'),  # GET, PUT, DELETE (detail)
    path('comment/add/<int:song_id>/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
