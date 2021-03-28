from django.urls import path

from . import views

urlpatterns = [
    path('orders/assign/', views.assign, name='assign orders'),
    path('orders/complete/', views.complete, name='complete order'),
    path('test/', views.test, name='test'),
    path('couriers/', views.couriers, name='post couriers'),
    path('couriers/<int:courier_id>', views.edit, name='courier'),
    path('orders/', views.orders, name='post orders'),
]
