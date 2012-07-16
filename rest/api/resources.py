from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from rest.models import Island, Message

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()

class IslandResource(ModelResource):
    class Meta:
        queryset = Island.objects.all()

class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
