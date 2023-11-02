from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Jedi


# Define the home view
def home(request):
  return render(request, 'home.html')

class CustomJediCreateView(CreateView):
    model = Jedi
    fields = ['name', 'planet', 'age', 'lightsabercolor', 'jeditype']
    success_url = '/home/'

    def form_valid(self, form):
        # Assign specific stats based on Jedi type before saving the form
        jedi_type = form.cleaned_data['jeditype']
        stats = get_jedi_stats(jedi_type)
        form.instance.powerlevel = stats['power_level']
        form.instance.lightsaberskill = stats['lightsaber_skills']
        form.instance.forceabilities = stats['force_abilities']
        form.instance.defense = stats['defense']
        form.instance.agility = stats['agility']
        form.instance.wisdom = stats['wisdom_knowledge']
        form.instance.stamina = stats['stamina_endurance']
        form.instance.charisma = stats['charisma_influence']
        return super().form_valid(form)

