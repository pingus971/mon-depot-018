from django import forms

# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)
#
from django.forms import ModelForm, Textarea
#
# from polls.models import ImageBrute
#
# class ImageForm(ModelForm):
#     class Meta:
#         model = ImageBrute
#         fields = ['photo']

from pavage.models import ChargerImage
class ChargerImageForm(ModelForm):
    class Meta:
        model = ChargerImage
        fields = ['photo']