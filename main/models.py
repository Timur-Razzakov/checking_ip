from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from .utils import unique_slug_generator


class Country(models.Model):
    name = models.CharField(verbose_name='country_name', max_length=255)

    def __str__(self):
        return self.name


class Url(models.Model):
    description = models.TextField(verbose_name='text', blank=True,
                                   null=True)
    link = models.CharField(verbose_name='link_name', max_length=255)

    def __str__(self):
        return "%s" % self.link


class Country_link(models.Model):
    link_name = models.ForeignKey(Url, verbose_name='url_id', on_delete=models.CASCADE,
                                  blank=True, null=True, related_name="link_names")
    country_name = models.ManyToManyField(Country, related_name="country_names")
    new_url = models.CharField(verbose_name='new_link', max_length=255, unique=True)
    comment = models.TextField(verbose_name='comment', blank=True,
                               null=True)

    def __str__(self):
        return self.new_url

    def get_absolute_url(self):
        return reverse('myurl', kwargs={'url': self.new_url})


"""Сохраняем в модель Country_link сгенерированные ссылки"""


# генерация происходит в utils.py
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.new_url:
        instance.new_url = unique_slug_generator(instance)


post_save.connect(pre_save_receiver, sender=Country_link)
