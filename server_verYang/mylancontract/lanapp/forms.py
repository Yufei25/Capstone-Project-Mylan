from django import forms

from lanapp.models import *


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


class ContractCommentForm(forms.Form):
    comment = forms.CharField(max_length=2000,
                              widget=forms.TextInput())

    def clean(self):
        cleaned_data = super(ContractCommentForm, self).clean()

        comment = cleaned_data.get('comment')

        if not comment:
            raise forms.ValidationError("Contract Comment Error!")

        return cleaned_data


class ContentCommentForm(forms.Form):
    comment = forms.CharField(max_length=2000,
                              widget=forms.TextInput())

    def clean(self):
        cleaned_data = super(ContentCommentForm, self).clean()

        comment = cleaned_data.get('comment')

        if not comment:
            raise forms.ValidationError("Content Comment Error!")

        return cleaned_data


class WarningCommentForm(forms.Form):
    comment = forms.CharField(max_length=2000,
                              widget=forms.TextInput())

    def clean(self):
        cleaned_data = super(WarningCommentForm, self).clean()

        comment = cleaned_data.get('comment')

        if not comment:
            raise forms.ValidationError("Warning Comment Error!")

        return cleaned_data
