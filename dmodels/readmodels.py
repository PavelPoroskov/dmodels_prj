import inspect


from django.db import models


from dmodels import fieldrules


def getModels(_models):

	list_Models = [{ 
		'model': model, 
		'table_name': name, 
		'table_title': model._meta.verbose_name 
		} for (name,model) in vars(_models).items() 
		if inspect.isclass(model) and issubclass( model, models.Model ) ]
	
	return list_Models

def getFields(_Model):

	list_fields = [{
		'id' : field.name,
#			'title' : field.description,
		'title' : field.verbose_name,
		'type' : fieldrules.dictFieldToStrType[type(field)],
		} for field in _Model._meta.fields if type(field) in fieldrules.dictFieldToStrType ]

	return list_fields

