from django.contrib import admin
from . import models

@admin.register(models.Room)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'room_num', 'price', 'minPerson', 'maxPerson', 'detail', 'isFree', 'exp_date')

admin.site.register(models.RoomType)