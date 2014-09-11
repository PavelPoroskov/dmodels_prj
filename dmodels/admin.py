from django.contrib import admin

# Register your models here.

#from dmodels.models import dictModelClasses

#for v in dictModelClasses.values():
#	admin.site.register( v )

from dmodels import models
from dmodels.models import dictModelStructure

for model_name in dictModelStructure.keys():
	admin.site.register( getattr( models, model_name ) )
