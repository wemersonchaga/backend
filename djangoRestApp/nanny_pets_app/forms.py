from django import forms
from .models import Cuidador

class ImagemAmbienteBatchUploadForm(forms.Form):
    cuidador = forms.ModelChoiceField(queryset=Cuidador.objects.all())
    fotos = forms.FileField(widget=forms.ClearableFileInput(), required=False)
