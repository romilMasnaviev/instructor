from django.db import models

class Parachutist(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    experience_level = models.CharField(max_length=100)

    def __str__(self):
        return self.name

