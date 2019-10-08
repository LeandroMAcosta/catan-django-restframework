from django.contrib import admin
from .models import Hex, VertexPosition, Game

admin.site.register(VertexPosition)
admin.site.register(Hex)
admin.site.register(Game)
