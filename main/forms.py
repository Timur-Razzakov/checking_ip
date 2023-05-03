from ckeditor.widgets import CKEditorWidget
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


class UrlForm(forms.ModelForm):
    url_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Введите url, через запятую или вводите по одному',
    )
    description = forms.CharField(widget=CKEditorWidget(),
                                  required=False,
                                  label='Место для коммента!!')  # max_file_size=1024 * 1024 * 5
    class Meta:
        model = Url
        fields = ('url_name','description')

    def clean(self, *args, **kwargs):
        get_urls = self.cleaned_data.get('url_name').split(',')
        if get_urls:
            for item in get_urls:
                qs = Url.objects.filter(link=item)
                if qs.exists():
                    raise forms.ValidationError('Такой Url уже существует!!')
                else:
                    pass
            return super(UrlForm, self).clean()


class CountryForm(forms.ModelForm):
    country_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   label='Введите country, через запятую или вводите по одному',
                                   )

    class Meta:
        model = Country
        fields = ('country_name',)

    def clean(self, *args, **kwargs):
        get_country_names = self.cleaned_data.get('country_name').split(',')
        if get_country_names:
            for item in get_country_names:
                qs = Country.objects.filter(name=item.upper())
                if qs.exists():
                    raise forms.ValidationError('Такой Country уже существует!!')
                else:
                    pass
            return super(CountryForm, self).clean(*args, **kwargs)
