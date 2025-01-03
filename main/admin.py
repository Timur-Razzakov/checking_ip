from django import forms
from django.contrib import admin
from .models import Url, Country, Country_link
from django.utils.html import strip_tags


class UrlAdmin(admin.ModelAdmin):
    list_display = ('link', 'description', 'id',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


class Country_linkAdmin(admin.ModelAdmin):
    list_display = ('link_name', 'comment', 'get_country', 'new_url', 'id',)

    def get_country(self, obj):
        return "\n".join([country.name for country in obj.country_name.all()])


admin.site.register(Url, UrlAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Country_link, Country_linkAdmin)
