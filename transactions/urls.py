from django.urls import path, include
from rest_framework import routers

from .views import *

# Non-Nested Routers
router = routers.DefaultRouter()
# router.register('products', ProductViewSet)
urlpatterns = [
    path('', include(router.urls)),

]
