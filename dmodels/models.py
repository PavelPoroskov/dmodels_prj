from django.conf import settings

#from dmodels.fix import IntegerField
from dmodels import loadmodels


loadmodels.loadFromYaml( settings.DMODELS_SCHEME_YAMLFILE, __name__ )

