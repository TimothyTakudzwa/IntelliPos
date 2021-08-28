from django.contrib import admin
from django.urls import path, include
from merchant.views import PostTransactionsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('user_auth.urls')),
    path('api/v1/', include('merchant.urls')),
    path('api/v1/transactions/', PostTransactionsView.as_view()),
   
]
