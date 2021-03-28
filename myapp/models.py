from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Courier(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    type = models.CharField(max_length=4, choices=[("foot", "foot"), ("car", "car"), ("bike", "bike")])
    weight_remained = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)
    regions = ArrayField(models.IntegerField())
    working_hours = ArrayField(models.CharField(max_length=11))
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)
    earnings = models.IntegerField(default=0)
    orders = models.ManyToManyField('Order', default=None, blank=True)

    def __str__(self):
        return str(self.id)+str(self.type)


class Order(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    weight = models.DecimalField(max_digits=4, decimal_places=2, validators=[MaxValueValidator(50), MinValueValidator(0.01)])
    region = models.IntegerField()
    delivery_hours = ArrayField(models.CharField(max_length=11))
    assign_time = models.DateTimeField(default=None, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    complete_time = models.DateTimeField(default=None, null=True, blank=True)
