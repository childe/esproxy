from django.contrib import admin
from esauth.models import ESAuth

class ESAuthAdmin(admin.ModelAdmin):
    list_display = ('index','index_regexp', 'username', 'group', 'allowed', 'action')
    list_filter = ('index_regexp', 'username', 'group')
    search_fields = ('index_regexp', 'username', 'group')

admin.site.register(ESAuth,ESAuthAdmin)
