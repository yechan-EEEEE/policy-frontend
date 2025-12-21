from django.contrib import admin
from .models import Policy

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['plcyNo', 'plcyNm', 'lclsfNm', 'mclsfNm', 'sprvsnInstCdNm']
    search_fields = ['plcyNm', 'plcyExplnCn']
    list_filter = ['lclsfNm', 'mclsfNm', 'sprvsnInstCdNm']