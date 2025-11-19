from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.forms.models import model_to_dict
import json

from .models import Booking

def booking_page(request):
    return render(request, 'restaurant/booking.html')

def reservations_page(request):
    return render(request, 'restaurant/reservations.html')

@csrf_exempt
def bookings(request):
    if request.method == 'GET':
        date_param = request.GET.get('date')

        if date_param:
            date_obj = parse_date(date_param)
            filtered = Booking.objects.filter(reservation_date=date_obj)

            if not filtered.exists():
                return JsonResponse({
                    "message": "No booking for this date"
                }, status=200)

            data = [model_to_dict(b) for b in filtered]
            return JsonResponse(data, safe=False, status=200)

        all_bookings = Booking.objects.all()
        data = [model_to_dict(b) for b in all_bookings]
        return JsonResponse(data, safe=False, status=200)

    if request.method == 'POST':
        body = json.loads(request.body)

        name = body.get("first_name")
        date = body.get("reservation_date")
        slot = body.get("reservation_slot")

        date_obj = parse_date(date)

        exists = Booking.objects.filter(
            reservation_date=date_obj,
            reservation_slot=slot
        ).exists()

        if exists:
            return JsonResponse({
                "error": "Slot already booked"
            }, status=400)

        new = Booking(
            first_name=name,
            reservation_date=date_obj,
            reservation_slot=slot
        )
        new.save()

        return JsonResponse(model_to_dict(new), status=201)
