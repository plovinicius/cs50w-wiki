from django import forms


class CreateForm(forms.Form):
    title = forms.CharField(label='Title', required=True, max_length=100)
    content = forms.CharField(widget=forms.Textarea, required=True, label='Content')
