from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from rest.models import Island, Message
from tastypie import fields


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        allowed_methods = ['get']

class IslandResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner', full=True)
    class Meta:
        queryset = Island.objects.all()
        filtering = {
            'name': ['exact'],
            'rank': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'lon': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'lat': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        ordering = ['rank']

class MessageResource(ModelResource):
    dest = fields.ForeignKey(IslandResource, 'dest')
    class Meta:
        queryset = Message.objects.all()
        filtering = {
            'dest': ['exact'],
            'date': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'author': ['exact'],
            'topic': [],
        }
        ordering = ['date']
