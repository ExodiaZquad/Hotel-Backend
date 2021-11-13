from django.db import models

class RoomType(models.Model):
    type = models.CharField(max_length=1)
    max_price = models.IntegerField()
    min_price = models.IntegerField()
    type_name = models.CharField(max_length=20)
    room_free = models.IntegerField()
    rating = models.FloatField()
    pic = models.URLField()

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=50)
    room_num = models.IntegerField()
    price = models.IntegerField()
    # person_per_room = models.CharField(max_length=10)
    minPerson = models.IntegerField()
    maxPerson = models.IntegerField()
    detail = models.TextField()
    pic = models.URLField()
    isFree = models.BooleanField(default=True)
    exp_date = models.DurationField(blank=True, null=True)