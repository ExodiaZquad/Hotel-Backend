from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomTypeSerializer
from users.serializers import UserSerializer
from users.models import User
from core.settings import SECRET_KEY
import jwt, random, datetime, pytz

#implementing Tree


#implementing sorting algorithm
def bubbleSort(arr, **kwargs):
    method = kwargs['method']
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if(method == "isFree"):
                if(arr[i][method] < arr[j][method]):
                    arr[i], arr[j] = arr[j], arr[i]
            elif(arr[i][method] > arr[j][method]):
                arr[i], arr[j] = arr[j], arr[i]

#quick sort
def partition(start, end, array):
    pivot_index = start 
    pivot = array[pivot_index]["price"]
    while start < end:
        while start < len(array) and array[start]["price"] <= pivot:
            start += 1
        while array[end]["price"] > pivot:
            end -= 1
        if(start < end):
            array[start], array[end] = array[end], array[start]
    array[end], array[pivot_index] = array[pivot_index], array[end]
    return end
      
def quickSort(start, end, array):
    if (start < end):
        p = partition(start, end, array)
        quickSort(start, p - 1, array)
        quickSort(p + 1, end, array)
          
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
    if l < n and arr[largest]['price'] < arr[l]['price']:
        largest = l
    if r < n and arr[largest]['price'] < arr[r]['price']:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)

#insertion sort for sorting by room_num
def insertionSort(arr):
    lists = [x for x in arr]
    sortedList = [lists.pop(0)]
    while lists:
        poppy = lists.pop(0)
        for i in range(len(sortedList) - 1, -1, -1):
            if poppy['room_num'] > sortedList[i]['room_num']:
                sortedList.insert(i+1, poppy)
                break
            if i == 0:
                sortedList.insert(0, poppy)
                break
    return sortedList


#selection sort for min_person
def selectionSort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx]["min_person"] > arr[j]["min_person"]:
                min_idx = j
    arr[i], arr[min_idx] = arr[min_idx], arr[i]


#binary search using in api/room/<int:pk>/
def binarySearch(arr, l, r, pk):
    while l <= r:
        mid = l + (r - l) // 2;
        # Check if x is present at mid
        if arr[mid].id == pk:
            return mid
        # If x is greater, ignore left half
        elif arr[mid].id < pk:
            l = mid + 1
        # If x is smaller, ignore right half
        else:
            r = mid - 1
    # If we reach here, then the element
    # was not present
    return -1

def findRoomByRoomType(roomType):
    rooms = Room.objects.all()
    rooms = sorted(rooms, key=lambda item: item.id)
    ret = []
    for room in rooms:
        if(room.room_type == roomType):
            ret.append(room)
    return ret

def getThreeRoomFromDifferentType(room):
    roomType = int(room.room_type)
    ret = []
    for i in range(1,5):
        if(roomType != i):
            lst = findRoomByRoomType(i)
            ret.append(lst[random.randint(0, len(lst)-1)])
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
            return Response({"message": "headers not found"}, status=400)
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
        #implementing binary search to find the specific room
        query_set = Room.objects.all()
        rooms = [room for room in query_set]
        rooms = sorted(rooms, key=lambda item: item.id)
        #before do binarySearch the list need to be sorted first
        index = binarySearch(rooms, 0, len(rooms)-1, pk)
        if(index == -1):
            return Response({"message": "room not found"}, status=404)
        room = rooms[index]

        ret = getThreeRoomFromDifferentType(room)

        #implement bubble sort here to sort the price of the random three room
        for i in range(len(ret)):
            for j in range(i+1, len(ret)):
                if(ret[i].price > ret[j].price):
                    ret[i], ret[j] = ret[j], ret[i]

        #insert the room to the first index
        ret.insert(0, room)

        serializer = RoomSerializer(ret, many=True)
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
        if('type' not in request.headers.keys() or 'key' not in request.headers.keys() or 'isFree' not in request.headers.keys()):
            return Response(status=400)

        key = request.headers['key']
        valid_keys = ['room_num', 'price', 'min_person', 'isFree']
        if(key not in valid_keys):
            return Response({"message": "wrong key"}, status=400)

        isFree = request.headers['isFree']
        #return room with room_type specified
        room_type = request.headers['type']
        ret = findRoomByRoomType(int(room_type))

        #if key == isFree need to search
        rooms = []
        if(isFree == '1'):
            for room in ret:
                if(room.isFree == True):
                    rooms.append(room)
        else:
            for room in ret:
                if(room.isFree == False):
                    rooms.append(room)

        serializer = RoomSerializer(rooms, many=True)
        arr = [x for x in serializer.data]
        
        # using different sorting algorithm for different key
        if(key == "room_num"):
            arr = insertionSort(arr)
        elif(key == "min_person"):
            selectionSort(arr)
        elif(key == "price"):
            bubbleSort(arr, method="price")
            # heapSort(arr)

        # bubbleSort(arr, method=key)
        return Response(data=arr)

# api/room/book/<int:pk>/
class RoomBookView(APIView):
    def post(self, request, *args, **kwargs):
        #check for authentication key
        if('token' not in request.headers.keys()):
            raise AuthenticationFailed('Unauthenticated!')
        token = request.headers['token']
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['user_id']).first()

        req = request.data
        try:
            from_date_str = req['from']
            exp_date_str = req['to']
        except:
            raise ParseError({"message": "input not accepted"})
        # print(datetime.datetime.fromisoformat(from_date), datetime.datetime.fromisoformat(exp_date))

        from_date = datetime.datetime.fromisoformat(from_date_str)
        exp_date = datetime.datetime.fromisoformat(exp_date_str)

        pk = self.kwargs['pk']
        #implementing binary search to find the specific room
        query_set = Room.objects.all()
        rooms = [room for room in query_set]
        rooms = sorted(rooms, key=lambda item: item.id)
        #before do binarySearch the list need to be sorted first
        index = binarySearch(rooms, 0, len(rooms)-1, pk)
        if(index == -1):
            return Response({"message": "room not found"}, status=404)
        room = rooms[index]

        #change isFree to False, and add exp_date
        if(room.isFree):
            room.isFree = False
            room.from_date = from_date
            room.exp_date = exp_date
            room.save()
        else:
            return Response({"message": "Room not available"}, status=400)

        room_booked_str = user.room_booked
        room_booked_lst = strToList(room_booked_str)
        room_booked_lst.append(room.id)
        room_booked_str = listToStr(room_booked_lst)

        user.room_booked = room_booked_str
        user.save()
        #debug
        print(f'user : {user.id} have booked room number : {user.room_booked}')

        return Response({"message": "Booking Completed"}, status=202)


# api/room/check/date/
class RoomCheckDate(APIView):
    def get(self, request, *args, **kwargs):
        #check for authentication key
        if('token' not in request.headers.keys()):
            raise AuthenticationFailed('Unauthenticated!')
        token = request.headers['token']
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        # user = User.objects.filter(id=payload['user_id']).first()

        rooms = Room.objects.all()
        # serializer = RoomSerializer(rooms, many=True)
        utc = pytz.UTC
        for room in rooms:
            now = datetime.datetime.now().replace(tzinfo=utc)
            exp_date = room.exp_date
            if(exp_date):
                #check if the room is available
                if(now > exp_date):
                    #change isFree to True, exp_date to None
                    room.isFree = True
                    room.exp_date = None
                    room.from_date = None
                    room.save()
                    #debug
                    print(f'room number : {room.id} is now available.')

        users = User.objects.all()

        for user in users:
            room_booked_str = user.room_booked
            room_booked_lst = strToList(room_booked_str)
            temp = [x for x in room_booked_lst]

            for room_id in temp:
                r = Room.objects.get(pk=room_id)
                if(r.isFree):
                    room_booked_lst.remove(room_id)

            room_booked_str = listToStr(room_booked_lst)

            user.room_booked = room_booked_str
            user.save()

        return Response({"message": "success"}, status=200)


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

def listToStr(lst):
    s = ''
    for i in range(len(lst)):
        s += str(lst[i])
        if(i != len(lst) - 1):
            s += ', '
    return s

def strToList(s):
    if(len(s) == 0):
        return [] 
    return [int(x) for x in s.split(',')]