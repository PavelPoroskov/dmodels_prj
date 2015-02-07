from datetime import datetime
import collections
import json

from dmodels import readmodels

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


	listFields = readmodels.getFields(_Model)

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

	listFieldInfo = readmodels.getFields(_Model)
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
