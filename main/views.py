import os

import requests
from django.contrib.gis.geoip2 import GeoIP2
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # для запрета если не вошёл в систему
from django.contrib import messages
from .forms import Country_linkForm, UrlForm, CountryForm
from .models import Country, Url, Country_link


def home_view(request):
    return render(request, 'home.html')


"""Добавляем  новые ссылки и для них разрешённые города"""


@login_required
def add_params_view(request):
    global get_country
    form = Country_linkForm(request.POST or None)
    if form.is_valid():
        new_collect = form.save()
        data = form.cleaned_data
        new_collect.link_name = data['url']
        new_collect.comment = data['comment']
        for item in data['country']:
            new_collect.country_name.add(Country.objects.get(name=item))
        new_collect.save()
        messages.success(request, 'Данные Добавлены!!')
        return redirect('add_params')
    return render(request, 'add_params.html', {'form': form})


def get_ip(data):
    """Функция для получения ip клиента"""
    x_forwarded_for = data.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = data.META.get('REMOTE_ADDR')
    return ip


def client_data(client_ip):
    """Получаем дополнительную информацию о пользователе с сайта ip-api.com """
    ip_api = os.environ.get('SITE_FOR_GET_DATA_ABOUT_CLIENT')  # API, для получения данных
    params_for_ip = os.environ.get('PARAMS')  # параметры которые, нужно получить от API

    # получаем данные о пользователе
    url = f"{ip_api}{client_ip}?fields={params_for_ip}"
    response = requests.get(url)
    return response


# def check_url_view(request, url):
#     result = {}
#     geo = GeoIP2()
#     ip = get_ip(request)
#     result['about_user'] = client_data(ip).json()
#     # узнаём страну у полученного ip
#     geo_user = geo.country(ip)['country_code']
#     try:
#         country_id = Country.objects.get(name=geo_user)
#         get_need_url = Country_link.objects.filter(new_url=os.environ.get('IP_ADDRESS') + '/' + url,
#                                                    country_name=country_id.id
#                                                    ).values('link_name', 'country_name')
#         if get_need_url.exists():
#             for item in get_need_url:
#                 country = Country.objects.get(id=item['country_name'])
#                 url = Url.objects.get(id=item['link_name'])
#                 result['country'] = country.name
#                 result['url'] = url.link
#         else:
#             result['url'] = None
#             result['country'] = None
#     except Exception:
#         result['url'] = None
#         result['country'] = None
#     return JsonResponse(result)
#
"""Новая версия с использование редиректа по указанным ссылкам"""


def check_url_view(request, url):
    result = {}
    geo = GeoIP2()
    ip = get_ip(request)
    # узнаём страну у полученного ip
    geo_user = geo.country(ip)['country_code']
    try:
        country_id = Country.objects.get(name=geo_user)
        get_need_url = Country_link.objects.filter(new_url=os.environ.get('IP_ADDRESS') + '/' + url,
                                                   country_name=country_id.id
                                                   ).values('link_name', 'country_name')
        if get_need_url.exists():
            for item in get_need_url:
                url = Url.objects.get(id=item['link_name'])
                return HttpResponseRedirect(url.link)
        else:
            return HttpResponseRedirect(
                'https://doc-hosting.flycricket.io/giga-b-privacy-policy/e6c0c55a-98ec-42f2-9954'
                '-d858f42013dd/privacy')
    except Exception as e:
        return HttpResponseRedirect(
            'https://doc-hosting.flycricket.io/giga-b-privacy-policy/e6c0c55a-98ec-42f2-9954-d858f42013dd'
            '/privacy')


"""Функция для показа всех ссылок и стран"""


@login_required
def show_data_view(request):
    data = Country_link.objects.all().values('link_name__link', 'country_name__name', 'new_url')
    #  баг с именем 'maincountrynone', при первом создании появляется
    # content = {'new_url': 'maincountrynone'}
    # for item in data:
    #     if item['new_url'] in content['new_url']:
    #         pass
    #     content['country_name'] = item
    return render(request, "get_all_urls.html", {'data': data})


"""Функция для сохранения страны через форму"""


@login_required
def add_country_view(request):
    country_form = CountryForm(request.POST or None)
    if country_form.is_valid():
        new_country = country_form.save()
        data = country_form.cleaned_data
        country = data['country_name'].split(',')
        new_country.name = country[0].upper()
        new_country.save()
        for item in country[1::]:
            save_country = Country.objects.create()
            save_country.name = item.upper()
            save_country.save()
        messages.success(request, 'Успешно Добавлены!!')
        return redirect('add_country')
    return render(request, 'add_country.html', {'country_form': country_form})


"""Функция для сохранения ссылки через форму"""


@login_required
def add_url_view(request):
    url_form = UrlForm(request.POST or None)
    if url_form.is_valid():
        new_url = url_form.save()
        data = url_form.cleaned_data
        url = data['url_name'].split(',')
        new_url.link = url[0]
        new_url.save()
        for item in url[1::]:
            save_url = Url.objects.create()
            save_url.link = item
            save_url.save()
        messages.success(request, 'Успешно Добавлены!!')
        return redirect('add_url')
    return render(request, 'add_url.html', {'url_form': url_form})
