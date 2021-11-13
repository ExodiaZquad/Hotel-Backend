from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer

#implementing Tree


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

    def put(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if(serializer.is_valid()):
            roomtype = RoomType.objects.get(pk=room.id)
            room_free = roomtype.room_free
            if(room.isFree and request.data['isFree'] == False):
                room_free = roomtype.room_free - 1
            elif(room.isFree == False and request.data['isFree'] == True):
                room_free = roomtype.room_free + 1
            roomTypeSerializer = RoomTypeSerializer(roomtype, data={
                'type': roomtype.type,
                'max_price': roomtype.max_price,
                'min_price': roomtype.min_price,
                'type_name': roomtype.type_name,
                'room_free': room_free,
                'rating': roomtype.rating,
                'pic': roomtype.pic
            })
            serializer.save()
            if(roomTypeSerializer.is_valid()):
                roomTypeSerializer.save()
            print(roomtype.room_free)
            return Response(serializer.data) 
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        room = generics.get_object_or_404(Room.objects.all(), pk=pk)
        room.delete()
        return Response({"message": f"Room with {pk} has been removed"}, status=204)

class RoomTypeView(APIView):
    # queryset = RoomType.objects.all()
    # serializer_class = RoomTypeSerializer
    def get(self,request, *args, **kwargs):
        roomTypes = RoomType.objects.all()
        serializer = RoomTypeSerializer(roomTypes, many=True)
        return Response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        roomType = RoomType.objects.get(pk=self.kwargs['pk'])
        serializer = RoomTypeSerializer(roomType, data=request.data)
        print(roomType.type_name)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        serializer = RoomTypeSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RoomSortView(APIView):
    def get(self, request, *args, **kwargs):
        key = request.headers['key']
        valid_keys = ['room_num', 'price', 'minPerson', 'isFree']
        if(key not in valid_keys):
            return Response({"message": "wrong key"}, status=400)
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        arr = [x for x in serializer.data]
        bubbleSort(arr, method=key)
        return Response(data=arr)