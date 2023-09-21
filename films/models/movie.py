from django.db import models
from .actor import Actor

class Movie(models.Model):
    name = models.CharField(max_length=250, blank=False,null=False)
    year = models.IntegerField(blank=True, default=0)
    imdb = models.DecimalField(max_digits=3, decimal_places=1)
    GENRE_CHOICES=(
        ('action','Action'),
        ('comedy','Comedy'),
        ('drama','Drama'),
        ('horror','Horror'),
    )
    genre = models.CharField(max_length=250, choices=GENRE_CHOICES)
    actors=models.ManyToManyField(Actor, related_name='movies')
    def __str__(self):
        return self.name
