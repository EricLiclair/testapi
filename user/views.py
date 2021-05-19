from django.db.models import query
from .models import User
from .serializers import *
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_and_authenticate_user

# Token Authentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import BasicAuthentication

from .authentication import BearerTokenAuthentication

# permissions
from rest_framework.permissions import IsAuthenticated


# temporary get all users view
class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


# get bearer token
class GetTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'bearer': token.key,
                'user': UserSerializer(user).data
            }
        )


# create a new user
class CreateUserView(generics.CreateAPIView):
    serializer_class = AuthSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            encrypted_data = request.data.copy()
            encrypted_password = make_password(request.data.get('password'))
            encrypted_data['password'] = encrypted_password

            serializer = self.get_serializer(data=encrypted_data)
            serializer.is_valid(raise_exception=True)

            # using the serializer.save method instead of perform_create()
            # to access the object to be used for
            user = serializer.save()
            headers = self.get_success_headers(serializer.data)
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'Error': 'Already logged in'}, status=status.HTTP_403_FORBIDDEN)


# get details of a particular user
class GetUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    authentication_classes = [BearerTokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# update a user
class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    authentication_classes = [BearerTokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        username = self.kwargs['username']
        if request.user.get_username() == username:  # only update self
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({'Error': 'Not Allowed'}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        username = self.kwargs['username']
        if request.user.get_username() == username:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'Error': 'Not Allowed'}, status=status.HTTP_403_FORBIDDEN)


# login
class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.is_authenticated:
            user = get_and_authenticate_user(**serializer.validated_data)
            login(request, user)
            data = UserSerializer(user).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Already logged in', 'User': UserSerializer(request.user).data}, status=status.HTTP_403_FORBIDDEN)


# logout
class LogoutUserView(APIView):

    def get(self, request):
        logout(request)
        return Response('Logged Out!', status=status.HTTP_200_OK)
