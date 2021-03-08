from django.urls import path, include
from django.contrib.auth.models import User
from .views import UserViewSet, TransactionViewSet
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt import views as jwt_views
from api import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'transactions', TransactionViewSet )

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/<int:id>/', views.TransactionViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

