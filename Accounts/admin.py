from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(StdDetails)
admin.site.register(OrgDetails)
admin.site.register(Blog)
admin.site.register(News)