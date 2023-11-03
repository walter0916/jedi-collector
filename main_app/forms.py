from django.forms import ModelForm
from .models import Training, Mission
from django import forms

class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = ['date', 'type']
        widgets = {
            'date': forms.DateInput(attrs={'id': 'id_date_training'}),
        }

class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = ['date', 'type']
        widgets = {
            'date': forms.DateInput(attrs={'id': 'id_date_mission'}),
        }
