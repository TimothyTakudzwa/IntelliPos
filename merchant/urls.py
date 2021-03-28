from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from merchant import views
from .views import *

router = routers.DefaultRouter()
router.register('merchants', MerchantProfileViewSet) 

# Nested
# Merchant
# merchants/                                                create
# merchant/{pk}                                             retrieve/update/delete

# Merchant Banks
# merchant/{pk}/banks/                                      create/list
# merchant/{pk}/banks/{pk}                                  retrieve/update/delete

# Merchant POS terminals
# merchants/{pk}/pos_terminals/                             create/list
# merchants/{pk}/pos_terminals/{pk}                         (re)assign/retrieve/update/delete

# Merchant Operators
# merchants/{pk}/operators/                                 create/list                         
# merchants/{pk}/pos_terminals/{pk}                         (re)assign/retrieve/update/delete


# Non-Nested Routers

# pos_terminals/                                             create/list
# pos_terminals?merchant_id=123                              retrieve/update/delete

# operators/                                                 create/list
# operators?merchant_id=1                                    retrieve/update/delete


urlpatterns = [
    path('', include(router.urls)),

]

