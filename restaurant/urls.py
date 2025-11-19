from django.urls import path
from . import views

urlpatterns = [
    path('booking', views.booking_page, name='booking_page'),
    path('reservations', views.reservations_page, name='reservations_page'),
    path('bookings', views.bookings, name='bookings'),
]