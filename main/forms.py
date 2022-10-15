from .models import Country_link, Country, Url
from django import forms

"""Форма для объединения страны и ссылки"""


class Country_linkForm(forms.ModelForm):
    country = forms.ModelMultipleChoiceField(
        label='Выберите страны для которых должна работать ссылка',
        queryset=Country.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    url = forms.ModelChoiceField(
        queryset=Url.objects.all(),
        to_field_name="link",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите ссылку '
    )

    class Meta:
        model = Country_link
        fields = ('country', 'url')
