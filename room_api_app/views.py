
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


from .models import Room
from .serializers import RoomSerializer, UsageSerializer
from .util import get_usages


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        """ Must be Admin user to perform create, update, and destroy methods. """

        if self.action in ['list', 'retrieve', 'usage', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, pk=None):
        """ Normal user can update availability but not name. Will return a 403 if the user tries to change name. """

        if not self.request.user.is_staff and "name" in self.request.data:
            return Response(status=status.HTTP_403_FORBIDDEN)  # should this be a 400?

        try:
            room = Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def usage(self, request):
        """ Lists any time the availablity of a room was changed. """

        id = request.GET.get('roomId')
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')

        """ Ensure all parameters are provided. """
        if not all([start_date, end_date, id]):
            content = {'detail': 'start date, end date, and room id must be provided as query string parameters.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        """ Ensure that room ID is a positive integer. """
        if not request.GET.get('roomId').isdigit():
            content = {'detail': 'room id should be a positive integer.'}
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(pk=id)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        histories = room.history.filter(history_date__range=[start_date, end_date])
        serializer = UsageSerializer(get_usages(room, histories), many=True)

        if not serializer.data:
            content = {'detail': 'no usage between given dates.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)
