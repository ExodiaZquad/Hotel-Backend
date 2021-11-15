from django.contrib import admin
from . import models

@admin.register(models.Room)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'room_num', 'price', 'min_person', 'max_person', 'detail', 'isFree', 'exp_date')

admin.site.register(models.RoomType)