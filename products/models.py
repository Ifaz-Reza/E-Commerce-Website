from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField()
    image_url = models.CharField(max_length=2083)
    details = models.CharField(max_length = 500)
    












