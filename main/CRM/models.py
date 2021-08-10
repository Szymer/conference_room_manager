from django.db import models


# Create your models here.
class ConfRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField()
    has_projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class RoomReservation(models.Model):
    reservation_date = models.DateField()
    room_id = models.ForeignKey(ConfRoom, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)

    class Meta:
        unique_together = ("reservation_date", "room_id",)
