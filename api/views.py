from rest_framework import generics, status
from .models import Profile
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from user.authentication import BearerTokenAuthentication
from rest_framework.response import Response


def testview(request, *args, **kwargs):
    return Response("Hello World. Lets test this api", status=status.HTTP_200_OK)


class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # using the serializer.save method instead of perform_create()
            # to access the object to be used for
            profile = serializer.save(user=user)
            headers = self.get_success_headers(serializer.data)

            data = ListProfileSerializer(profile).data
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response({'Error': 'A Profile already exists.'})


class ListProfileView(generics.ListAPIView):
    serializer_class = ListProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]


class GetProfileView(generics.RetrieveAPIView):
    serializer_class = ListProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]


class UpateProfileView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user.get_username() == profile.user.get_username():  # only update self
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
        profile = self.get_object()
        if request.user.get_username() == profile.user.get_username():  # only update self
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'Error': 'Not Allowed'}, status=status.HTTP_403_FORBIDDEN)
