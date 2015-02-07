from django.conf import settings


from dmodels import loadmodels


loadmodels.loadFromYaml( settings.DMODELS_SCHEME_YAMLFILE, __name__ )

