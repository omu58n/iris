from django.db import models

class Iris(models.Model):
    sepalLength = models.FloatField()
    sepalWidth = models.FloatField()
    petalLength = models.FloatField()
    petalWidth = models.FloatField()
    result = models.CharField(max_length=20)
