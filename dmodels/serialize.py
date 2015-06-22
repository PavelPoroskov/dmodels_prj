from datetime import datetime
import collections
import json

from django.utils.encoding import smart_unicode

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
		'model': _Model.__name__,
		'fields': listFields,
		'data': new_data
		})

	return res_str

def serialize_ssv( _data, _Model, _errors=None ):

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

#	print('serialize 0')
	if _errors is None:
#		print('serialize 1')
		if not isinstance(_data, collections.Sized):
			_data = [_data]


		new_data = [object_to_arr( row, listFields ) for row in _data]

		res_str = json.dumps({
			'result': 'Ok',
			'model': _Model.__name__,
			'fields': listFields,
			'data': new_data
			})
	else:
#		print('serialize 2')

		new_data=[]
		"""
		for field in listFields:
			field_id = field['id']
			print('field_id ' + field_id)
			value = getattr( _data, field_id )
#			if field['type'] == 'date':
#				value = value.strftime( '%m/%d/%Y' )

			new_row.append( value )
		"""

#		print('serialize 22')
		res_str = json.dumps({
			'result': 'Error',
			'model': _Model.__name__,
			'fields': listFields,
			'data': new_data,
			'errors': _errors
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

def deserialize_ssv( request_POST, _Model ):

	listFieldInfo = readmodels.getFields(_Model)
	dictFields = { finfo['id']: finfo['type'] for finfo in listFieldInfo }

	dictValues = {}					
	for (field, value) in request_POST.items():
		if (field in dictFields):
#			if dictFields[field] == 'int': 
#				value = int(value)
#				if isinstance(value, unicode):
#					value = value.encode('ascii','replace')
#			elif dictFields[field] == 'date': 
#				value = datetime.strptime( value, '%m/%d/%Y' )

			dictValues[field] = value

	return dictValues
