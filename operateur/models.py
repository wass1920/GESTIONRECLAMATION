from django.db import models

class Operateur(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    numtel = models.CharField(max_length=15)
    password = models.CharField(max_length=255)

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    drone_choices = [
        ('orange', 'orange'),
        ('TT', 'TT'),
    ]
    operateur = models.CharField(max_length=100, choices=drone_choices, default='orange')


class Claim(models.Model):
    text = models.TextField()
    user = models.CharField(max_length=100)
    operator=models.CharField(max_length=100)
    heure=models.CharField(max_length=100)
