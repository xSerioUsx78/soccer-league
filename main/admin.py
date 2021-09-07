from django.contrib import admin
from .models import Tour, Team, Match, Week

# Register your models here.


admin.site.register(Tour)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Week)