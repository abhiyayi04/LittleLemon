from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from .models import Booking
from .views import bookings
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date


class BookingModelTest(TestCase):
    def test_create_booking(self):
        booking = Booking.objects.create(
            first_name="Abhi",
            reservation_date=date(2025, 1, 10),
            reservation_slot=3
        )
        expected_str = f"Abhi - 2025-01-10 @ 3"
        self.assertEqual(str(booking), expected_str)


class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Booking.objects.create(
            first_name="John",
            reservation_date=date(2025, 2, 5),
            reservation_slot=1
        )
        Booking.objects.create(
            first_name="Sarah",
            reservation_date=date(2025, 2, 6),
            reservation_slot=2
        )

    def test_get_bookings(self):
        response = self.client.get("/bookings")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)


class BookingURLTest(TestCase):
    def test_bookings_url_resolves_to_view(self):
        resolver = resolve("/bookings")
        self.assertEqual(resolver.func, bookings)
