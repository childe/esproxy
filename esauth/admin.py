from django.contrib import admin
from esauth.models import ESAuth

class ESAuthAdmin(admin.ModelAdmin):
    list_display = ('index','request_method', 'uri_regexp', 'username', 'group', 'allowed')
    list_filter = ('request_method', 'uri_regexp', 'username', 'group')
    search_fields = ('request_method', 'uri_regexp', 'username', 'group')

admin.site.register(ESAuth,ESAuthAdmin)
