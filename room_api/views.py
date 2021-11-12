from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer

#implementing sorting algorithm
def bubbleSort(arr, **kwargs):
    method = kwargs['method']
    print(method)
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if(method == "isFree"):
                if(arr[i][method] < arr[j][method]):
                    arr[i], arr[j] = arr[j], arr[i]
            elif(arr[i][method] > arr[j][method]):
                arr[i], arr[j] = arr[j], arr[i]

class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetailView(APIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def get(self, request, *args, **kwargs):
       pk = self.kwargs['pk']
       room = Room.objects.filter(id=pk).first()
       if(room is None):
           return Response({"message": "Page Not Found!"}, status=404)
       serializer = RoomSerializer(room)
       return Response(serializer.data)

    def delete(self, request, pk):
        room = generics.get_object_or_404(Room.objects.all(), pk=pk)
        room.delete()
        return Response({"message": f"Room with {pk} has been removed"}, status=204)

class RoomTypeView(generics.ListCreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class RoomSortView(APIView):
    def get(self, request, *args, **kwargs):
        key = request.headers['key']
        valid_keys = ['room_num', 'price', 'minPerson', 'isFree']
        if(key not in valid_keys):
            return Response(status=400)
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        arr = [x for x in serializer.data]
        for i in range(len(arr)):
            print(arr[i][key], end=', ')
        print('')
        bubbleSort(arr, method=key)
        for i in range(len(arr)):
            print(arr[i][key], end=', ')
        print('')
        return Response({'message': 'successfully sorted'})