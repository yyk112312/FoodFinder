from django import forms
class Postsearch(forms.Form):
    search = forms.CharField(label='Search')