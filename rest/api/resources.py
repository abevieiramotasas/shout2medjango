from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from rest.models import Island, Message
from tastypie import fields

from tastypie.authorization import Authorization


##### testando #####

class AbAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        allowed_methods = ['get']
        include_resource_uri = False

    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)

class IslandResource(ModelResource):

    owner = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        queryset = Island.objects.all()
        filtering = {
            'name': ['exact'],
            'rank': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'longitude': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'latitude': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        ordering = ['rank']
        include_resource_uri = False
        authorization = AbAuthorization()

        
    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)


class MessageResource(ModelResource):

    dest = fields.ForeignKey(IslandResource, 'dest')

    class Meta:
        queryset = Message.objects.all()
        filtering = {
            'dest_id': ['exact'],
            'date': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'author': ['exact'],
            'topic': [],
        }
        ordering = ['date']
        include_resource_uri = False

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(MessageResource, self).build_filters(filters)

        if "dest_id" in filters:
            ms = Message.objects.all().filter(dest__id=filters['dest_id'])

            orm_filters["dest_id"] = ms

        return orm_filters
        
    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)


def clean_data_dict(data_dict):
    if isinstance(data_dict, dict):
        del(data_dict['meta'])
    return data_dict
