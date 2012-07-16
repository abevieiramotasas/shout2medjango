from django.contrib.gis import admin
from models import Island, Message

admin.site.register(Island, admin.ModelAdmin)
admin.site.register(Message, admin.ModelAdmin)
