from django import forms
from .models import Team


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }