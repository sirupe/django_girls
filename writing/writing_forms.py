from django import forms


class WritingForm(forms.Form):
    title = forms.CharField(label='제목', max_length=1000)
    contents = forms.CharField(label='내용', max_length=100000, widget=forms.Textarea)
    tags = forms.CharField(label='태그', max_length=1000)