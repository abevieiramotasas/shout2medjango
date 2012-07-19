from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from rest.models import Island, Message
from tastypie import fields

from tastypie.authorization import Authorization


##### testando #####

# ver authorization e authentication
class AbAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True


class UserResource(ModelResource):

    class Meta:
        # queryset base
        queryset = User.objects.all()
        # campos do resource que irao ser retornados
        # pode-se usar excludes = [...] para indicar os campos que nao serao retornados
        fields = ['username']
        # metodos http permitidos
        allowed_methods = ['get']
        # se a uri do resource vai ser retornada como parte dos campos do resource
        include_resource_uri = False
        
    # retiro informacoes meta do resource
    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)
        
        
class IslandResource(ModelResource):
    # indico que o campo owner deve ser mostrado com todas informacoes do resource
    # no caso, UserResource, no lugar(default) de ele retornar a uri do resource
    # ira retornar os campos do resource
    owner = fields.ForeignKey(UserResource, 'owner', full=True)
    
    class Meta:
        queryset = Island.objects.all()
        # indico, para cada campo, quais sao os filtros permitidos
        # para utilizar os filtros na url, deve-se passa-los como query-param
        # como seria feito num filter do queryset do django
        # ex: .../island/?name=ilha&rank__lt=10.0&...&format=json
        # ! ele nao detecta query-params invalidos
        filtering = {
            'name': ['exact'],
            'rank': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'longitude': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'latitude': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        # indica que campo pode ser usado em ordenacao
        # ex: ../island/?order_by=rank&format=json 
        # pode usar -rank para indicar ordem inversa
        ordering = ['rank']
        include_resource_uri = False
        
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
            'topic': ['exact'],
        }
        ordering = ['date']
        include_resource_uri = False

    # adiciono um filtro para retornar apenas mensagens da ilha cujo id for passado
    # necessario porque o tastypie nao implementa filtro em campos de resource que eh campo do resource
    # da pra entender nao ne? hehe
    # nao pode fazer, por exemplo, .../message/?destination_id=10&format=json
    def build_filters(self, filters=None):
        # verifica se ha filtros, caso nao, cria dict vazio
        if filters is None:
            filters = {}
        # gera os filtros
        orm_filters = super(MessageResource, self).build_filters(filters)
        
        # se a request pede pra usar o filtro dest_id
        if "dest_id" in filters:
            # informar o queryset desse filtro
            # filters[<nome do filtro>] informa o valor passado pro filtro
            ms = Message.objects.all().filter(dest__id=filters['dest_id'])
            # adiciona o queryset
            orm_filters["dest_id"] = ms
        # retorna o dic de querysets
        # ! ver como funciona a aplicacao de varios filtros
        return orm_filters
        
    def alter_list_data_to_serialize(self, request, data_dict):
        return clean_data_dict(data_dict)

# metodo para remover informacoes meta do resource
def clean_data_dict(data_dict):
    if isinstance(data_dict, dict):
        del(data_dict['meta'])
    return data_dict
