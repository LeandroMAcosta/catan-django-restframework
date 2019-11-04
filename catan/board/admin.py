from django.contrib import admin
from .models import Board, Hexagon


class BoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Board, BoardAdmin)
admin.site.register(Hexagon)
