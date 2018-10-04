from django.urls import reverse
from django.test import TestCase

from .models import City, Hotel


class ViewTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            id="AMS",
            city="Amsterdam",
        )
        self.hotel = Hotel.objects.create(
            city = self.city,
            id="AMSN",
            hotel="Kraan Hotel Amsterdam Noord",
        )


    def test_view_cities(self):
        resp = self.client.get(reverse('locations:cities'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.city, resp.context['cities'])
        self.assertTemplateUsed(resp, 'locations/cities.html')
        self.assertContains(resp, self.city.city)

    def test_view_hotels(self):
        resp = self.client.get(reverse('locations:hotels'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.hotel, resp.context['hotels'])
        self.assertTemplateUsed(resp, 'locations/hotels.html')
        self.assertContains(resp, self.hotel.hotel)

    def test_view_city(self):
        resp = self.client.get(reverse('locations:city', kwargs={'city_name':self.city.city}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.city, resp.context['city'])
        self.assertTemplateUsed(resp, 'locations/city.html')
        self.assertContains(resp, self.city.city)
        self.assertContains(resp, self.hotel.hotel)