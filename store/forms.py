from django.forms import ModelForm, Textarea
from .models import ContactModel, ReviewModel
from django import forms


class ContactForm(ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'


class ReviewForm(ModelForm):
    class Meta:
        model = ReviewModel
        fields = ('name', 'review')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', ' placeholder': ' Name'}),
            'review': forms.Textarea(attrs={'class': 'form-control', ' placeholder': ' Comment'}),

        }
        labels = {
            'name': '',
            'review': '',
        }
