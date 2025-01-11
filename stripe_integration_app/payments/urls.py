from django.urls import path
from . import views

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('cancel/',views.cancel,name='cancel'),
    path('success/',views.success,name='success'),
    path('webhook/',views.stripe_webhook,name='stripe-webhook'),
]
