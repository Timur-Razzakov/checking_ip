
from django.contrib.gis.geoip2 import GeoIP2
from django.http import JsonResponse
from django.shortcuts import render, redirect
# from icecream import ic
from django.contrib import messages
from .forms import Country_linkForm, UrlForm, CountryForm
from .models import Country, Url, Country_link


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
        messages.success(request, 'Данные Добавлены!!')
        return redirect('add_params')
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
        get_need_url = Country_link.objects.filter(new_url='143.47.237.139/' + url, country_name=country_id.id
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
    content = {'new_url': 'maincountrynone'}
    for item in data:
        if item['new_url'] in content['new_url']:
            pass
        content['country_name'] = item
    return render(request, "get_all_urls.html", {'data': data})


"""Функция для сохранения страны через форму"""


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
