from django.db import models


class Team(models.Model):
    TEAM_CHOICES = (
        ('RED', 'Team Red'),
        ('BLUE', 'Team Blue'),
        ('YELLOW', 'Team Yellow')
    )
    name = models.CharField(
        max_length=10,
        choices=TEAM_CHOICES,
        default='RED',
    )
    points = models.IntegerField()


class User(models.Model):

    user_name = models.CharField(max_length=30)

    facebook_id = models.CharField(max_length=50)

    team = models.ForeignKey('Team', models.CASCADE)

    points = models.IntegerField()

    def __str__(self):
        return self.user_name


class Hotspot(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    #team = models.ForeignKey('Team', models.CASCADE)
    frequency = models.IntegerField()

    class Meta:
        unique_together = (("longitude", "latitude"),)


class Bin(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    team = models.ForeignKey('Team', models.CASCADE)
    frequency = models.IntegerField()

    class Meta:
        unique_together = (("longitude", "latitude"),)


