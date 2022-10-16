from django.http import JsonResponse
from django.shortcuts import render

from .forms import Country_linkForm
from .models import Country, Url, Country_link
from icecream import ic
from django.contrib.gis.geoip2 import GeoIP2


def home_view(request):
    return render(request, 'home.html')


"""Добавляем  новые ссылки и для них разрешённые города"""


def add_params_view(request):
    global get_country
    form = Country_linkForm(request.POST or None)
    if form.is_valid():
        new_collect = form.save()
        data = form.cleaned_data
        new_collect.link_name = data['url']
        for item in data['country']:
            new_collect.country_name.add(Country.objects.get(name=item))
        new_collect.save()
        return render(request, 'home.html', {'new_collect': new_collect})
    return render(request, 'add_params.html', {'form': form})


"""Получаем user_ip"""


def check_url_view(request, url):
    # получаем ip клиента
    data = {}
    geo = GeoIP2()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
        # узнаём страну у полученного ip
    geo_user = geo.country(ip)['country_code']
    try:
        country_id = Country.objects.get(name=geo_user)
        get_need_url = Country_link.objects.filter(new_url=url, country_name=country_id.id
                                                   ).values('link_name', 'country_name')
        if get_need_url.exists():
            for item in get_need_url:
                country = Country.objects.get(id=item['country_name'])
                url = Url.objects.get(id=item['link_name'])
                data['country'] = country.name
                data['url'] = url.link
        else:
            data['url'] = None
            data['country'] = None
    except Exception:
        data['url'] = None
        data['country'] = None
    return JsonResponse(data)


"""Функция для показа всех ссылок и стран"""

def show_data_view(request):
    data = Country_link.objects.all().values('link_name', 'country_name', 'new_url')
    content = {}
    for item in data:
        ic(item['new_url'])
        if item['new_url'] in content['new_url']:
            pass
        content['country_name'] = item
    return render(request, "get_all_urls.html", {'data': data})
