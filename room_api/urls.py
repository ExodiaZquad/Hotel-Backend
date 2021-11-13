from rest_framework import routers, urlpatterns
from .views import RoomListView, RoomDetailView, RoomTypeView, RoomSortView 
from django.urls import path

app_name = 'room_api'

urlpatterns = [
    path('api/room/', RoomListView.as_view()),
    path('api/room/<int:pk>/', RoomDetailView.as_view()),
    path('api/roomtype/', RoomTypeView.as_view()),
    path('api/room/sort/', RoomSortView.as_view()),
]

# router = routers.DefaultRouter()
# router.register(r'', RoomListView, basename='room_list')
# router.register(r'/<int:pk>', RoomDetailView, basename='room_detail')

# urlpatterns = router.urls