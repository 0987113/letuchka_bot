from django import forms

from .models import Profile
from .models import Definition
from .models import Category


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = (
            'profile',
            'category',
        )
        widgets = {
            'category': forms.TextInput,
        }


class DefForm(forms.ModelForm):

    class Meta:
        model = Definition
        fields = (
            'profile',
            'category',
            'text',
            'header',

        )
        widgets = {
            'header': forms.TextInput,
        }




