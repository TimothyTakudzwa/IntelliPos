from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from api import views
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'transactions', TransactionViewSet )

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/<int:id>/', views.TransactionViewSet.as_view()),
    path('login/', views.LoginViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get_token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

