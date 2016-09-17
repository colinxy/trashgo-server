from django.db import models


class Location(models.Model):
    user = models.ForeignKey('User', models.CASCADE)
    time = models.DateTimeField()
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return '{} , {}'.format(self.longitude, self.latitude)


class User(models.Model):
    TEAM_CHOICES = (
        ('RED', 'Team Red'),
        ('BLUE', 'Team Blue'),
        ('YELLOW', 'Team Yellow')
    )

    user_name = models.CharField(max_length=30)

    facebook_id = models.CharField(max_length=50)

    team = models.CharField(
        max_length=10,
        choices=TEAM_CHOICES,
        default='RED',
    )

    points = models.IntegerField()

    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.user_name


class Hotspot(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    frequency = models.IntegerField()

    def __str__(self):
        return '{}, {}, {}visits'.format(self.longitude,
                                         self.latitude,
                                         self.frequency)
