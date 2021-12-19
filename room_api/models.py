from django.db import models

class RoomType(models.Model):
    type = models.CharField(max_length=1)
    max_price = models.IntegerField()
    min_price = models.IntegerField()
    type_name = models.CharField(max_length=20)
    room_free = models.IntegerField()
    rating = models.FloatField()
    pic1 = models.URLField()
    pic2 = models.URLField()
    pic3 = models.URLField()

class Room(models.Model):
    # room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_type = models.IntegerField()
    room_name = models.CharField(max_length=50)
    room_num = models.IntegerField()
    price = models.IntegerField()
    # person_per_room = models.CharField(max_length=10)
    min_person = models.IntegerField()
    max_person = models.IntegerField()
    detail = models.TextField(blank=True)
    #Change these to CharField
    pic1 = models.CharField(max_length=100)
    pic2 = models.CharField(max_length=100)
    pic3 = models.CharField(max_length=100)
    isFree = models.BooleanField(default=True)
    # exp_date = models.DurationField(blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    exp_date = models.DateTimeField(blank=True, null=True)