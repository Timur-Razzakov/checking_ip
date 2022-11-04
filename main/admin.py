from django import forms
from django.contrib import admin
from .models import Url, Country, Country_link


class UrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'link','description')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class Country_linkAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_name', 'get_country', 'new_url')

    def get_country(self, obj):
        return "\n".join([country.name for country in obj.country_name.all()])


admin.site.register(Url, UrlAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Country_link, Country_linkAdmin)
