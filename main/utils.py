import os
import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_url=None):
    if new_url is not None:
        return new_url

    new_url = slugify(instance.country_name)
    Klass = instance.__class__

    while Klass.objects.filter(new_url=new_url).exists():
        # Если new_url уже существует, генерируем новый
        new_url = "{ip_address}/{randtext}-{randstr}".format(
            ip_address=os.environ.get('IP_ADDRESS'),
            randtext=random_string_generator(size=6),
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_url=new_url)
    return new_url



