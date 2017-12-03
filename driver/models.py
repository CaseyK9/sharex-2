from django.db import models
from django.conf import settings

class Car(models.Model):
    TYPE_CHOICES = (
        (1, 'truck'),
        (2, 'pickup'),
        (3, 'van'),
        (4, 'eco_car'),
        (5, 'SUV'),
        (6, 'sport_car'),
        (7, 'pickup'),
    )
    account = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    _type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    plate = models.CharField(max_length=30)
    _model = models.CharField(max_length=255)
    year = models.CharField(max_length=4)

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    timeupdate = models.DateTimeField(auto_now=True)

    class Meta:
    	ordering = ['-timestamp']

    def __str__(self):
        return self.account.get_short_name() + " " + self.plate


class Travel(models.Model):
    car = models.ForeignKey(Car,blank=True,null=True)
    depart_location = models.TextField(blank=True,null=True)
    depart_latitute = models.TextField(blank=True,null=True)
    depart_longtitute = models.TextField(blank=True,null=True)
    arrive_location = models.TextField(blank=True,null=True)
    arrive_latitute = models.TextField(blank=True,null=True)
    arrive_longtitute = models.TextField(blank=True,null=True)
    current_location = models.TextField(blank=True,null=True)
    current_latitute = models.TextField(blank=True,null=True)
    current_longtitute = models.TextField(blank=True,null=True)
    is_complete = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    timeupdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.car.plate + " " + self.depart_location + " to " +self.arrive_location + " " + str(self.is_complete)
		