# Generated by Django 4.1.2 on 2023-05-02 20:51

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_url_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='description link'),
        ),
    ]
