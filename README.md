[![Build Status](https://travis-ci.org/johnpooch/room_api.svg)](https://travis-ci.org/johnpooch/room_api)

# API for Room Monitoring System

### API Specifications

The room monitoring system allows users to see if a meeting room is in use and to view the history of room usage. Any member of staff view the status of any room and change that status. Only administrators can add new rooms and change the name of a room. Each room has: (1) a unique ID; (2) a name (max 50 characters); (3) an availability state (true or false).

### API Overview

The API was built using the Django REST Framework. Room usage was tracked using the 'Django-Simple-History' app. The API was run in the local environment using Docker. The API was deployed to Heroku. However, I was not able to deploy to Heroku using Docker.

### Reasoning for Technical Choices

The Django REST framework was chosen for a number of reasons. I have prior experience working with Django and I enjoy writing in Python. The browsable API makes it easy to visualise the structure of the API. Users and permissions can be easily implemented using Django. There is a lot of documentation and community info available.

Django Simple History was used because the Django framework already records changes made to models. This means that only a small change to the code was necessary to implement the usage feature. Django Simple History records extra information about changes which could be useful for future improvements.

In order to present the usage feature in the specified format, I created a Usage class which stored the room information as well as the relevant usage information. I created a UsageSerializer which rendered the usage in the specified format.

I used a ViewSet for listing, retrieving, creating, updating, and destroying rooms. Within this ViewSet, I specified a 'usage' action which handled the usage feature. This operated more like a typical Django view. A function called 'get_usage' [room_api_app/util.py] was used to get only the histories in which the availability state was changed (as per the spec).

Freezegun was used in order to test the usage feature which relies on time parameters.

### Suggestions for Future Improvements

The code allowing basic users to change the availability of a room but not change the name is not a very elegant solution. The solution doesn't work in the web browsable API which is frustrating. I would like to improve this by adding permissions to the individual fields of the Room serializer. Alternatively, I could use two separate serializers, BasicRoomSerializer and FullRoomSerializer, and mark 'name' as a read_only field on the BasicRoomSerializer. I tried to implement both of these solutions but couldn't get it to work how I wanted. I would benefit from a greater understanding of serializers and how permissions are handled with Django REST.

I would like to work out how to deploy the containerised version to Heroku. I followed the documentation but ran into problems that I could not work around. A deeper understanding of Docker might be necessary.

Some of the code in the testing script is repetitive. I would like to spend more time refactoring that code.

### Live Version

Live version: https://room-api-johnpooch.herokuapp.com/api/

##### Pre-canned Users

(1) Username: admin, Password : P^55w0rd1, Permissions: all permissions
(2) Username: admin_user, Password : P^55w0rd1, Permissions: IsAdminUser
(3) Username: staff_user, Password : P^55w0rd1, Permissions: IsAuthenticated

### Running Locally

Clone this workspace and install the dependencies:

```
$ git clone git@github.com:johnpooch/room_api.git
$ cd  room_api
$ pip3 install -r requirements.txt
```

Create a file called '.env':

```
$ touch .env
```

Inside env paste in the following and replace <secret_key> with a secret key (https://www.miniwebtool.com/django-secret-key-generator/):

```
SECRET_KEY='<secret_key>'
```

Migrate to database:

```
$ python3 manage.py migrate
```

You'll need to create a superuser to log in to the app:

```
$ python3 manage.py createsuperuser
```

You should now be able to run the site locally using Docker:

```
$ docker-compose up
```

To create more users, navigate to the admin panel - http://0.0.0.0:8000/admin/

### Running the tests

To carry out the automated tests:

```
$ python3 manage.py test
```

## Built With

-   [Django](https://www.djangoproject.com/) - The Django web framework.
-   [Heroku](https://www.heroku.com) - Used for deployment.
-   [Travis](https://www.travis-ci.org) - Used for continuous integration.
-   [Docker](https://www.docker.com) - Used for containerisation.
