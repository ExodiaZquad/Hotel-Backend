from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from .models import User
from core.settings import SECRET_KEY
from room_api.models import Room
from room_api.serializers import RoomSerializer
import jwt

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        pass

class LogoutView(APIView):
    def post(self, request):
        pass

class UserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        if('token' not in request.headers.keys()):
            raise AuthenticationFailed('Unauthenticated!')
        token = request.headers['token']
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        # note-to-self: maybe make this more secure (sending only user_id?)
        ret = []
        ret.append(serializer.data)

        room_booked_str = user.room_booked
        room_booked_lst = strToList(room_booked_str)
        for room_id in room_booked_lst:
            room = Room.objects.get(pk=room_id)
            room_serializer = RoomSerializer(room)
            ret.append(room_serializer.data)

        return Response(ret, status=200)

def listToStr(lst):
    s = ''
    for i in range(len(lst)):
        s += str(lst[i])
        if(i != len(lst) - 1):
            s += ', '
    return s

def strToList(s):
    if(s):
        if(len(s) == 0):
            return [] 
        return [int(x) for x in s.split(',')]
    return []