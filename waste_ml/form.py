from django import forms
from .models import WasteImage

class WasteImageForm(forms.ModelForm):
    class Meta:
        model = WasteImage
        fields = ['image']