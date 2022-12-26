# Django
from django import forms

#model
from .models import ItemService

# Itemservice
class FormCreateItemservice(forms.ModelForm):
    """ Supplie update model form."""

    class Meta:
        """Form settings."""

        model = ItemService
        fields = ('service', 'article', 'amount')
        widgets = {
            'article' : forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
        }
