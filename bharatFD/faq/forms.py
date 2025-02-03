from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import FAQTranslation

class FAQTranslationForm(forms.ModelForm):
    """Custom form to resize CKEditor in Django Admin inline"""

    language = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:50px;'})
    )
    
    question = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:270px;'})
    )
    
    answer = forms.CharField(
        widget=CKEditorWidget(attrs={'style': 'width:600px; height:400px;'})
    )

    class Meta:
        model = FAQTranslation
        fields = "__all__"
