from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Jedi


# Define the home view
def home(request):
  return render(request, 'home.html')

class JediCreate(CreateView):
  model = Jedi
  fields = ['name', 'planet', 'age', 'lightsabercolor', 'jeditype', 'mentor']
  success_url = '/home/'

  def form_valid(self, form):
    jedi_type = form.cleaned_data['jeditype']
    stats = get_jedi_stats(jedi_type)
    form.instance.powerlevel = stats['power_level']
    form.instance.lightsaberskill = stats['lightsaberskills']
    form.instance.forceabilities = stats['forceabilities']
    form.instance.defense = stats['defense']
    form.instance.agility = stats['agility']
    form.instance.wisdom = stats['wisdom']
    form.instance.stamina = stats['stamina']
    form.instance.charisma = stats['charisma']
    return super().form_valid(form)

def get_jedi_stats(jedi_type):
  if jedi_type == 'consular':
    return {
      'powerlevel': 7,
      'lightsaberskills': 6,
      'forceabilities': 9,
      'defense': 7,
      'agility': 6,
      'wisdom': 10,
      'stamina': 7,
      'charisma': 8
    }
  elif jedi_type == 'sentinel':
    return {
      'powerlevel': 8,
      'lightsaberskills': 8,
      'forceabilities': 8,
      'defense': 8,
      'agility': 7,
      'wisdom': 8,
      'stamina': 8,
      'charisma': 7
    }
  elif jedi_type == 'guardian':
    return {
      'powerlevel': 9,
      'lightsaberskills': 9,
      'forceabilities': 7,
      'defense': 9,
      'agility': 7,
      'wisdom': 7,
      'stamina': 9,
      'charisma': 6
    }
  else:
    return {
      'power_level': 5,
      'lightsaberskills': 5,
      'forceabilities': 5,
      'defense': 5,
      'agility': 5,
      'wisdom': 5,
      'stamina': 5,
      'charisma': 5
    }