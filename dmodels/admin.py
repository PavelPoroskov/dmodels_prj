from django.contrib import admin

# Register your models here.

from dmodels.models import dictModelClasses

for v in dictModelClasses.values():
	admin.site.register( v )
