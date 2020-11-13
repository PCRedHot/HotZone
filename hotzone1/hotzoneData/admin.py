from django.contrib import admin

from .models import *

admin.site.register(Patient)
admin.site.register(Disease)
admin.site.register(Place)
admin.site.register(CasePlace)
admin.site.register(Case)
