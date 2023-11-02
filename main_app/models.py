from django.db import models

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

class Jedi(models.Model):
  name = models.CharField(max_length=100) 
  planet = models.CharField(
    max_length=1,
    choices=PLANET,
    default=PLANET[0][0]
    ) 
  age = models.IntegerField()
  lightsabercolor = models.CharField(max_length=100)
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
