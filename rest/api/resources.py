from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from rest.models import Island, Message
from tastypie import fields


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        allowed_methods = ['get']
        include_resource_uri = False
        
    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)
        
        
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
        include_resource_uri = False
        
    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)

class MessageResource(ModelResource):
    dest = fields.ForeignKey(IslandResource, 'dest')
    class Meta:
        queryset = Message.objects.all()
        filtering = {
            'dest': ['exact'],
            'date': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'author': ['exact'],
            'topic': ['exact'],
        }
        ordering = ['date']
        include_resource_uri = False
        
    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)
        
        
        
def clean_data_dict(data_dict):
    if isinstance(data_dict, dict):
        del(data_dict['meta'])
    return data_dict
