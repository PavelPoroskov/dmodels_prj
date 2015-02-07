
from django.contrib import admin
from django.db.models import Model

from dmodels import models
from dmodels import readmodels

for dictModelInfo in readmodels.getModels(models):
	admin.site.register( dictModelInfo['model'] )		
