from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer
from users.serializers import UserSerializer
from users.models import User
from core.settings import SECRET_KEY
import jwt

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

def findRoomByRoomType(roomType):
    rooms = Room.objects.all()
    ret = []
    for room in rooms:
        if(room.room_type == roomType):
            ret.append(room)
    return ret

# api/room
class RoomListView(APIView):
    def get(self, request, *args, **kwargs):
        #check for authentication key
        if('token' not in request.headers.keys()):
            raise AuthenticationFailed('Unauthenticated!')
        token = request.headers['token']
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['user_id']).first()

        #return room with room_type specified
        if('type' not in request.headers.keys()):
            return Response(status=400)
        rooms = Room.objects.all()

        room_type = request.headers['type']
        ret = findRoomByRoomType(int(room_type))

        serializer = RoomSerializer(ret, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# api/room/<int:pk>
class RoomDetailView(APIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def get(self, request, *args, **kwargs):
        #check for authentication key
        if('token' not in request.headers.keys()):
            raise AuthenticationFailed('Unauthenticated!')
        token = request.headers['token']
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['user_id']).first()

        pk = self.kwargs['pk']
        room = Room.objects.filter(id=pk).first()
        if(room is None):
            return Response({"message": "Page Not Found!"}, status=404)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        #check for authentication key
        if('token' not in request.headers.keys()):
            raise AuthenticationFailed('Unauthenticated!')
        token = request.headers['token']
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['user_id']).first()

        pk = self.kwargs['pk']
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if(serializer.is_valid()):
            roomtype = RoomType.objects.get(pk=room.room_type)
            room_free = roomtype.room_free
            if(room.isFree and request.data['isFree'] == False):
                room_free = roomtype.room_free - 1
            elif(room.isFree == False and request.data['isFree'] == True):
                room_free = roomtype.room_free + 1
            updateRoomType(roomtype, room_free)
            serializer.save()
            print(roomtype.room_free)
            return Response(serializer.data) 
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        room = generics.get_object_or_404(Room.objects.all(), pk=pk)
        room.delete()
        return Response({"message": f"Room with {pk} has been removed"}, status=204)

# api/roomtype/
class RoomTypeView(APIView):
    def get(self,request, *args, **kwargs):
        roomTypes = RoomType.objects.all()
        roomsQueryset = Room.objects.all()
        roomSerializer = RoomSerializer(roomsQueryset, many=True)
        rooms = [x for x in roomSerializer.data]
        lst = [0, 0, 0, 0]
        for room in rooms:
            pk = room['room_type']
            if(room['isFree'] == True):
                lst[pk-1] += 1
        print(lst)
        updateRoomType(RoomType.objects.get(pk=1), lst[0])
        updateRoomType(RoomType.objects.get(pk=2), lst[1])
        updateRoomType(RoomType.objects.get(pk=3), lst[2])
        updateRoomType(RoomType.objects.get(pk=4), lst[3])
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
        print(request.data)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# api/room/sort/
class RoomSortView(APIView):
    def get(self, request, *args, **kwargs):
        key = request.headers['key']
        valid_keys = ['room_num', 'price', 'min_person', 'isFree']
        if(key not in valid_keys):
            return Response({"message": "wrong key"}, status=400)
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        arr = [x for x in serializer.data]
        bubbleSort(arr, method=key)
        return Response(data=arr)

def updateRoomType(roomType, room_free):
    serializer = RoomTypeSerializer(roomType, data={
        'type': roomType.type,
        'max_price': roomType.max_price,
        'min_price': roomType.min_price,
        'type_name': roomType.type_name,
        'room_free': room_free,
        'rating': roomType.rating,
        'pic1': roomType.pic1,
        'pic2': roomType.pic2,
        'pic3': roomType.pic3
    })
    if(serializer.is_valid(raise_exception=True)):
       serializer.save()