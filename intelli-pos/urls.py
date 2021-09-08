from django.contrib import admin
from django.urls import path, include
from merchant.views import TransactionsView, GetTransactionsView, EmailTransactionsView
from product.views import PostProductView, SearchProductView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('user_auth.urls')),
    path('api/v1/', include('merchant.urls')),
    path('api/v1/transactions/', TransactionsView.as_view()),
    path('api/v1/transactions/<str:search>/', GetTransactionsView.as_view()),
    path('api/v1/transactions/receipt/<str:reference>/', EmailTransactionsView.as_view()),
    path('api/v1/shop/product/', PostProductView.as_view()),
    path('api/v1/shop/product/<str:code>/', SearchProductView.as_view()),
   
]
