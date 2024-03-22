from django import forms


class SearchForm(forms.Form):
    tags = forms.CharField(label='Tags', max_length=100)
