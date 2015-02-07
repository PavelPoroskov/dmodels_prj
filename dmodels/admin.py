
from django.contrib import admin
from django.db.models import Model

from dmodels import models
from dmodels import engine

for dictModelInfo in engine.getModels(models):
	admin.site.register( dictModelInfo['model'] )		
