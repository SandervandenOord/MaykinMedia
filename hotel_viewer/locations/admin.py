from django.contrib import admin

from .models import City, Hotel


class HotelInline(admin.StackedInline):
    model = Hotel


class CityAdmin(admin.ModelAdmin):
    inlines = [HotelInline, ]


# Register your models here.
admin.site.register(City, CityAdmin)
admin.site.register(Hotel)
