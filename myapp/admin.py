from django.contrib import admin
from django.contrib.auth.models import Group, User

from myapp.models import PUser, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    fields = ('name', 'price', 'p_user')


admin.site.register(PUser)
admin.site.unregister(Group)
admin.site.unregister(User)
