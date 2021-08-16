from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from merchant import views
from .views import *

# Non-Nested Routers
router = routers.DefaultRouter()
router.register('merchants', MerchantProfileViewSet) 
router.register('pos_terminals', POSTerminalViewSet, basename='POSTerminal') 
router.register('operators', OperatorProfileViewSet) 

# merchant/                                                 create/list
# merchant/<int:pk>/                                        retrieve/update/delete

# banks/                                                    create/list
# banks/<int:pk>/                                           retrieve/update/delete

# pos_terminals/                                             create/list
# pos_terminals/<int:pk>/                                    retrieve/update/delete
# pos_terminals/<int:pk>/assign_operator/                    assign operator

# operators/                                                 create/list
# operators/<int:pk>/                                        retrieve/update/delete


urlpatterns = [
    path('', include(router.urls)),

]