from django import forms

from pagedown.widgets import PagedownWidget

from .models import Simulation

class SimulationForm(forms.ModelForm):

    class Meta:
        model = Simulation
        fields = [
            "data", # by json
        ]