from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer

class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetailView(APIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def get(self, request, *args, **kwargs):
    #    print(request.headers['Key'])
       pk = self.kwargs['pk']
       room = Room.objects.filter(id=pk)
       if(room.exists() == False):
           return Response(status=404)
       serializer = RoomSerializer(room, many=True)
       return Response({"room": serializer.data})

    def delete(self, request, pk):
        room = generics.get_object_or_404(Room.objects.all(), pk=pk)
        room.delete()
        return Response({"message": f"Room with {pk} has been removed"}, status=204)

class RoomTypeView(generics.ListCreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer