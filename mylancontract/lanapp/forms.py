from django import forms

from models import *


class SearchResultForm(forms.ModelForm):
    class Meta:
        model = SearchResult
        exclude = ()
        # widgets = {'picture': forms.FileInput()}

    def clean(self):
        cleaned_data = super(SearchResultForm, self).clean()

        filename = cleaned_data.get('filename')
        keyword = cleaned_data.get('keyword')
        content = cleaned_data.get('content')

        if not filename:
            raise forms.ValidationError("Filename is required.")
        if not keyword:
            raise forms.ValidationError("Keyword is required.")
        if not content:
            raise forms.ValidationError("Content is required.")

        return cleaned_data
