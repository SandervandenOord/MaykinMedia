from django.shortcuts import render, get_list_or_404, get_object_or_404

from .models import Hotel, City


def hotels(request):
    hotels = get_list_or_404(Hotel)
    return render(request, 'locations/hotels.html', {'hotels': hotels})

def cities(request):
    cities = get_list_or_404(City)
    return render(request, 'locations/cities.html', {'cities': cities})

def city(request, city_name):
    city = get_object_or_404(City, city=city_name)
    return render(request, 'locations/city.html', {'city': city})