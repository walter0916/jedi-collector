from django.db import models
from django.urls import reverse
from datetime import date 

JEDITYPE = (
  ('C', 'Consular'),
  ('S', 'Sentinel'),
  ('G', 'Guardian'),
)

MENTOR = (
  ('Y', 'Yoda'),
  ('K', 'Kit Fisto'),
  ('O', 'Obi-Wan Kenobi'),
  ('M', 'Mace Windu'), 
  ('Q', 'Qui-Gon Jinn'),
  ('L', 'Luke Skywalker'),
  ('A', 'Anakin Skywalker'),
  ('C', 'Count Dooku')
)

PLANET = (
  ('T', 'Tatooine'),
  ('C', 'Coruscant'),
  ('N', 'Naboo'),
  ('K', 'Kamino'),
  ('D', 'Dagobah'), 
  ('A', 'Alderaan'),
  ('M', 'Mustafar'),
  ('J', 'Jakku'),
  ('B', 'Bespin')
)

COLOR = (
  ('B', 'Blue'),
  ('G', 'Green'),
  ('R', 'Red'),
  ('P', 'Purple'),
  ('Y', 'Yellow')
)

TRAINING = (
  ('L', 'Lightsaber Training'),
  ('M', 'Meditation'),
  ('S', 'Study of Jedi code'),
  ('T', 'Telekinesis'),
  ('F', 'Force Persuasion'),
  ('D', 'Diplomatic Training')
)

MISSION = (
  ('R', 'Rescue Mission'),
  ('A', 'Artifact Retrieval'),
  ('P', 'Peacekeeping'),
  ('I', 'Infiltration'),
  ('E', 'Exploration'), 
  ('S', 'Sabotage'),
  ('G', 'Guardian Mission'),
  ('C', 'Crisis Response'), 
  ('B', 'Bounty Hunter Pursuit')
)

class Jedi(models.Model):
  name = models.CharField(max_length=100) 
  planet = models.CharField(
    max_length=1,
    choices=PLANET,
    default=PLANET[0][0]
    ) 
  age = models.IntegerField()
  lightsabercolor = models.CharField(
    max_length=1,
    choices=COLOR,
    default=COLOR[0][0]
    )
  jeditype = models.CharField(
    max_length=1,
    choices=JEDITYPE,
    default=JEDITYPE[0][0]
    )
  mentor = models.CharField(
    max_length=1,
    choices=MENTOR,
    default=MENTOR[0][0]
    )
  powerlevel = models.IntegerField(default=0)
  lightsaberskill = models.IntegerField(default=0)
  forceabilities = models.IntegerField(default=0)
  defense = models.IntegerField(default=0)
  agility = models.IntegerField(default=0)
  wisdom = models.IntegerField(default=0)
  stamina = models.IntegerField(default=0)
  charisma = models.IntegerField(default=0)

  def __str__(self):
    return self.name
  
  def get_jeditype_display_value(self):
    return dict(JEDITYPE)[self.jeditype]
  
  def get_mentor_display_value(self):
    return dict(MENTOR)[self.mentor]
  
  def get_planet_display_value(self):
    return dict(PLANET)[self.planet]
  
  def get_lightsabercolor_display_value(self):
    return dict(COLOR)[self.lightsabercolor]

  def get_absolute_url(self):
    return reverse("jedi-detail", kwargs={"jedi_id": self.id})
  
  def trained_for_today(self):
    return self.training_set.filter(date=date.today()).count() >= len(TRAINING)
  
  def mission_for_today(self):
    return self.mission_set.filter(date=date.today()).count() >= 1
  
class Training(models.Model):
  date = models.DateField('Training Date')
  type = models.CharField(
    'Training Type',
    max_length=1,
    choices=TRAINING,
    default=TRAINING[0][0]
    )
  jedi = models.ForeignKey(Jedi, on_delete=models.CASCADE)

  def __str__(self):
      return f"{self.get_type_display()} on {self.date}"
  
class Mission(models.Model):
  date = models.DateField('Mission Date')
  type = models.CharField(
    'Mission Type',
    max_length=1,
    choices=MISSION,
    default=MISSION[0][0]
    )
  jedi = models.ForeignKey(Jedi, on_delete=models.CASCADE)
  
  def __str__(self):
      return f"{self.get_type_display()} on {self.date}"