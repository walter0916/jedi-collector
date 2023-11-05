from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Jedi, Mission
from .forms import TrainingForm, MissionForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import math 
import random
from datetime import date 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Define the home view
class Home(LoginView):
  template_name = 'home.html'

class JediCreate(LoginRequiredMixin, CreateView):
  model = Jedi
  fields = ['name', 'planet', 'age', 'lightsabercolor', 'jeditype', 'mentor']

  def form_valid(self, form):
    jedi_type = form.cleaned_data['jeditype']
    stats = get_jedi_stats(jedi_type)
    form.instance.powerlevel = stats['powerlevel']
    form.instance.lightsaberskill = stats['lightsaberskills']
    form.instance.forceabilities = stats['forceabilities']
    form.instance.defense = stats['defense']
    form.instance.agility = stats['agility']
    form.instance.wisdom = stats['wisdom']
    form.instance.stamina = stats['stamina']
    form.instance.charisma = stats['charisma']
    form.instance.user = self.request.user
    return super().form_valid(form)

def get_jedi_stats(jedi_type):
  if jedi_type == 'C':
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
  elif jedi_type == 'S':
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
  elif jedi_type == 'G':
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
  
class JediUpdate(UpdateView):
  model = Jedi 
  fields = ['name', 'planet', 'lightsabercolor', 'mentor']
  
class JediDelete(DeleteView):
  model = Jedi 
  success_url = '/jedi/'

@login_required
def jedi_index(request):
  jedis = Jedi.objects.filter(user=request.user)
  return render(request, 'jedis/index.html', {'jedis': jedis})

@login_required
def jedi_detail(request, jedi_id):
  jedi = Jedi.objects.get(id=jedi_id)
  training_form = TrainingForm()
  mission_form = MissionForm()
  return render(request, 'jedis/detail.html', {'jedi': jedi, 'training_form': training_form, 'mission_form': mission_form})

def add_training(request, jedi_id):
  jedi = Jedi.objects.get(id=jedi_id)
  form = TrainingForm(request.POST)
  if form.is_valid():
    new_training = form.save(commit=False)
    new_training.jedi_id = jedi_id
    new_training.save()
    if new_training.type == 'L':
      jedi.lightsaberskill = min(jedi.lightsaberskill + 1, 100)
      jedi.agility = min(jedi.agility + 1, 100)
      jedi.save()
    if new_training.type == 'M':
      jedi.stamina = min(jedi.stamina + 1, 100)
      jedi.charisma = min(jedi.charisma + 1, 100)
      jedi.save()
    if new_training.type == 'S':
      jedi.wisdom = min(jedi.wisdom + 1, 100)
      jedi.save()
    if new_training.type == 'T':
      jedi.forceabilities = min(jedi.forceabilities + 1, 100)
      jedi.save()
    if new_training.type == 'F':
      jedi.powerlevel = min(jedi.powerlevel + 1, 100)
      jedi.defense = min(jedi.defense + 1, 100)
      jedi.save()
    if new_training.type == 'D':
      jedi.charisma = min(jedi.charisma + 1, 100)
      jedi.save()
  return redirect('jedi-detail', jedi_id=jedi_id)


def calculate_success_probability(jedi, mission_type):
  mission_type_weights = {
    'R': {'agility': 0.5, 'lightsaberskill': 0.3, 'stamina': 0.2},  # Rescue Mission
    'A': {'wisdom': 0.4, 'forceabilities': 0.3, 'stamina': 0.3},  # Artifact Retrieval
    'P': {'wisdom': 0.4, 'charisma': 0.3, 'stamina': 0.3},  # Peacekeeping
    'I': {'wisdom': 0.4, 'forceabilities': 0.3, 'agility': 0.3},  # Infiltration
    'E': {'agility': 0.4, 'stamina': 0.3, 'lightsaberskill': 0.3},  # Exploration
    'S': {'agility': 0.4, 'forceabilities': 0.3, 'charisma': 0.3},  # Sabotage
    'G': {'charisma': 0.4, 'wisdom': 0.3, 'stamina': 0.3},  # Guardian Mission
    'C': {'charisma': 0.4, 'wisdom': 0.3, 'forceabilities': 0.3},  # Crisis Response
    'B': {'charisma': 0.4, 'agility': 0.3, 'forceabilities': 0.3}  # Bounty Hunter Pursuit
  }
    
  if mission_type in mission_type_weights:
    weights = mission_type_weights[mission_type]
    for stat, weight in weights.items():
      if jedi[stat] < 30:
        weights[stat] = weight * 0.005
    total_weighted_stats = sum(jedi[stat] * weight for stat, weight in weights.items())
    success_probability = 1 / (1 + math.exp(-total_weighted_stats))
    return success_probability
  else:
    return 0

def add_mission(request, jedi_id):
  jedi = Jedi.objects.get(id=jedi_id)
  form = MissionForm(request.POST)
  today = date.today()
  existing_mission = Mission.objects.filter(jedi_id=jedi_id, date=today).first()
  if existing_mission:
    return redirect('jedi-detail', jedi_id=jedi_id)
  if form.is_valid():
    new_mission = form.save(commit=False)
    new_mission.jedi_id = jedi_id
    mission_type = new_mission.type
    success_probability = calculate_success_probability({
      'agility': jedi.agility,
      'lightsaberskill': jedi.lightsaberskill,
      'wisdom': jedi.wisdom,
      'forceabilities': jedi.forceabilities,
      'stamina': jedi.stamina,
      'charisma': jedi.charisma,
      'defense': jedi.defense,
      'powerlevel': jedi.powerlevel
    }, mission_type)    
    random_number = random.random()
    if random_number <= success_probability:
      jedi.lightsaberskill = min(jedi.lightsaberskill + 5, 100)
      jedi.agility = min(jedi.agility + 5, 100)
      jedi.stamina = min(jedi.stamina + 5, 100)
      jedi.wisdom = min(jedi.wisdom + 5, 100)
      jedi.forceabilities = min(jedi.forceabilities + 5, 100)
      jedi.powerlevel = min(jedi.powerlevel + 5, 100)
      jedi.defense = min(jedi.defense + 5, 100)
      jedi.charisma = min(jedi.charisma + 5, 100)
      jedi.save()
    else:
      jedi.lightsaberskill = max(jedi.lightsaberskill - 5, 0)
      jedi.agility = max(jedi.agility - 5, 0)
      jedi.stamina = max(jedi.stamina - 5, 0)
      jedi.wisdom = max(jedi.wisdom - 5, 0)
      jedi.forceabilities = max(jedi.forceabilities - 5, 0)
      jedi.powerlevel = max(jedi.powerlevel - 5, 0)
      jedi.defense = max(jedi.defense - 5, 0)
      jedi.charisma = max(jedi.charisma - 5, 0)
      jedi.save()     
    new_mission.save()
  return redirect('jedi-detail', jedi_id=jedi_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('cat-index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

def about(request):
  return render(request, 'about.html')