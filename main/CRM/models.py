from django.db import models


# Create your models here.
class ConfRoom(models.Model):

    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField()
    has_projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name
