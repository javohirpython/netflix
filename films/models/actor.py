from django.db import models

class Actor(models.Model):
    name=models.CharField(max_length=250,blank=False,null=False)
    birthdate= models.DateField()
    GENDER_CHOICES=(
        ('male','Male'),
        ('female','Female'),
    )
    gender=models.CharField(max_length=250,choices=GENDER_CHOICES)

    def __str__(self):
        return self.name