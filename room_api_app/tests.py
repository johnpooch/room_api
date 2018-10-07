
from freezegun import freeze_time

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Room


class ApiRootTests(APITestCase):

    def test_cannot_get_api_root_when_not_logged_in(self):
        response = APIClient().get('/api/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_get_api_root_when_logged_in_as_user(self):
        test_user = User.objects.create_user(username='test_user', password='P^55w0rd1')
        test_user.save()
        c = APIClient()
        c.login(username='test_user', password='P^55w0rd1')
        response = c.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomViewsTests(APITestCase):

    def setUp(self):

        test_user = User.objects.create_user(username='test_user', password='P^55w0rd1')
        test_staff = User.objects.create_user(username='test_staff', password='P^55w0rd1')

        test_staff.is_staff = True

        test_user.save()
        test_staff.save()

        user = User.objects.get(username="test_staff")
        Room.objects.create(name='test_room', available=True, created_by=user)

    """ List Rooms """

    def test_cannot_get_room_list_when_not_logged_in(self):
        response = APIClient().get('/api/room/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_get_room_list_when_logged_in_as_user(self):
        c = APIClient()
        c.login(username='test_user', password='P^55w0rd1')
        response = c.get('/api/room/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_room_list_when_logged_in_as_admin(self):
        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        response = c.get('/api/room/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ Get Individual Rooms """

    def test_cannot_get_individual_room_when_not_logged_in(self):
        response = APIClient().get('/api/room/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # FAILING
    def test_can_get_individual_room_when_logged_in_as_user(self):
        c = APIClient()
        c.login(username='test_user', password='P^55w0rd1')
        response = c.get('/api/room/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_individual_room_when_logged_in_as_admin(self):
        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        response = c.get('/api/room/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ Create Rooms """

    def test_cannot_create_room_when_not_logged_in(self):
        response = APIClient().post('/api/room/', {'name': 'test_create_room', 'availablility': 'true'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_room_when_logged_in_as_user(self):
        c = APIClient()
        c.login(username='test_user', password='P^55w0rd1')
        response = c.post('/api/room/', {'name': 'test_create_room', 'available': 'true'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_room_when_logged_in_as_admin(self):
        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        response = c.post('/api/room/', {'name': 'test_create_room', 'available': True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 2)

    def test_cannot_create_room_with_name_already_in_use(self):
        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.post('/api/room/', {'name': 'test_create_room', 'available': True})
        response = c.post('/api/room/', {'name': 'test_create_room', 'available': True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Room.objects.count(), 2)

    def test_cannot_create_room_with_name_that_exceeds_50_chars(self):
        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        response = c.post('/api/room/', {'name': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'available': True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """ Update Rooms """

    def test_cannot_update_room_when_not_logged_in(self):
        response = APIClient().put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_room_when_logged_in_as_user(self):
        c = APIClient()
        c.login(username='test_user', password='P^55w0rd1')
        response = c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_room_when_logged_in_as_admin(self):
        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        response = c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Room.objects.get().name, 'test_room_edited')

    """ Delete Rooms """

    def test_cannot_delete_room_when_not_logged_in(self):
        response = APIClient().delete('/api/room/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_delete_room_when_logged_in_as_user(self):
        c = APIClient()
        c.login(username='test_user', password='P^55w0rd1')
        response = c.delete('/api/room/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_room_when_logged_in_as_admin(self):
        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        response = c.delete('/api/room/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UsageViewTests(APITestCase):

    @freeze_time("2000-02-01")
    def setUp(self):

        test_user = User.objects.create_user(username='test_user', password='P^55w0rd1')
        test_staff = User.objects.create_user(username='test_staff', password='P^55w0rd1')

        test_staff.is_staff = True

        test_user.save()
        test_staff.save()

        user = User.objects.get(username="test_staff")

        Room.objects.create(name='test_room', available=True, created_by=user)

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')

    @freeze_time("2000-02-02")
    def test_can_get_usage_when_usage_exists_between_given_dates(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&endDate=2000-03-01T00:00:00Z&roomId=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2000-04-01")
    def test_cannot_get_usage_when_usage_does_not_exist_between_given_dates(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&endDate=2000-03-01T00:00:00Z&roomId=1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2000-04-01")
    def test_cannot_get_usage_when_not_logged_in(self):

        c = APIClient()
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&endDate=2000-03-01T00:00:00Z&roomId=1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2000-02-02")
    def test_can_get_usage_when_logged_in_as_user(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        c.login(username='test_user', password='P^55w0rd1')
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&endDate=2000-03-01T00:00:00Z&roomId=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2000-02-02")
    def test_can_get_usage_when_logged_in_as_admin(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&endDate=2000-03-01T00:00:00Z&roomId=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2000-02-02")
    def test_returns_bad_request_when_start_date_is_not_given(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?endDate=2000-03-01T00:00:00Z&roomId=1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2000-02-02")
    def test_returns_bad_request_when_end_date_is_not_given(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&roomId=1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2000-02-02")
    def test_returns_bad_request_when_id_is_not_given(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&endDate=2000-03-01T00:00:00Z')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2000-02-02")
    def test_returns_404_when_room_id_invalid(self):

        c = APIClient()
        c.login(username='test_staff', password='P^55w0rd1')
        c.put('/api/room/1/', {'name': 'test_room_edited', 'availablility': 'true'})
        response = c.get('/api/room/usage/?startDate=2000-01-01T00:00:00Z&endDate=2000-03-01T00:00:00Z&roomId=2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
