
from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        remove_field = kwargs.pop('remove_field', None)
        super(RoomSerializer, self).__init__(*args, **kwargs)

        if remove_field:
            self.fields.pop(remove_field)

    class Meta:
        model = Room
        fields = ['id', 'name', 'available']


class UsageSerializer(serializers.Serializer):

    time = serializers.CharField()
    user = serializers.CharField()
    room = RoomSerializer(remove_field='available')
    available = serializers.CharField(required=False)
    name = serializers.CharField(required=False)


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())
