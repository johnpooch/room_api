
from django.urls import path, include

from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from .views import RoomViewSet


API_TITLE = 'Room Monitoring API'
API_DESCRIPTION = 'A Web API for viewing if a meeting room is in use and the history of room usage.'
schema_view = get_schema_view(title=API_TITLE)

router = routers.DefaultRouter()
router.register('room', RoomViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
]
