
from datetime import datetime
import collections
import json
import inspect


from django.db import models


fields = models.fields;

dictStrTypeToField = {
	"int":  { 'Field': fields.IntegerField, 'kwargs': {} },
	"char": { 'Field': fields.CharField, 'kwargs': { 'max_length': 30 } },
	"date": { 'Field': fields.DateField, 'kwargs': {} },
}

dictFieldToStrType = { value['Field']: key for key, value in dictStrTypeToField.items()}
dictFieldToStrType[fields.AutoField] = "int";


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
		'type' : dictFieldToStrType[type(field)],
		} for field in _Model._meta.fields if type(field) in dictFieldToStrType]

	return list_fields

def serialize( _data, _Model ):

	def object_to_arr( obj, listFields ):
		new_row = []
		for field in listFields:
			field_id = field['id']
			value = getattr( obj, field_id )
			if field['type'] == 'date':
				value = value.strftime( '%m/%d/%Y' )

			new_row.append( value )

		return new_row


	listFields = getFields(_Model)

	if not isinstance(_data, collections.Sized):
		_data = [_data]


	new_data = [object_to_arr( row, listFields ) for row in _data]

	res_str = json.dumps({
#		'model': model_name,
		'model': _Model.__name__,
		'fields': listFields,
		'data': new_data
		})

	return res_str

def deserialize( request_POST, _Model ):

	listFieldInfo = getFields(_Model)
	dictFields = { finfo['id']: finfo['type'] for finfo in listFieldInfo }

	dictValues = {}					
	for (field, value) in request_POST.items():
		if (field in dictFields):
			if dictFields[field] == 'int': 
				value = int(value)
			elif dictFields[field] == 'date': 
				value = datetime.strptime( value, '%m/%d/%Y' )

			dictValues[field] = value

	return dictValues
