
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, UsageSerializer
from .util import get_usages


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        """ Must be Admin user to perform create, update, and destroy methods. """

        if self.action in ['list', 'retrieve', 'usage']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

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
