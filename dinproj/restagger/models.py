from django.db import models

# User model creation.

class User(models.Model):
  name = models.CharField(max_length=50)
  company = models.CharField(max_length=50)
  designation = models.CharField(max_length=50)

  def __str__(self):
    return "%s, %s, %s " % (self.name, self.company, self.designation)
