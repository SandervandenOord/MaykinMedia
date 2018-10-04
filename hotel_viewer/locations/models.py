from django.db import models


class City(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.city

    class Meta:
        ordering = ['city',]


class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=10)
    hotel = models.CharField(max_length=255)

    def __str__(self):
        return self.hotel

    class Meta:
        ordering = ['hotel', 'id',]


