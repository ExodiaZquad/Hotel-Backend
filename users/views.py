from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from .models import User
from core.settings import SECRET_KEY
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        if('token' not in request.headers.keys()):
            # return Response({"message": "do not found token in the header"}, status=404)
            raise AuthenticationFailed('Unauthenticated!')
        token = request.headers['token']
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)