import os
import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_url=None):
    if new_url is not None:
        new_url = new_url
    else:
        new_url = slugify(instance.country_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(new_url=new_url).exists()
    if qs_exists:
        new_url = "{ip_address}/{new_url}-{randstr}".format(
            ip_address=os.environ.get('IP_ADDRESS'),
            new_url=new_url,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_url=new_url)
    return new_url



