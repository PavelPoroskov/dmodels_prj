from django.test import TestCase
from django.core.urlresolvers import reverse

from dmodels.models import dictModelClasses
from dmodels.models import dictModelStructure

from datetime import datetime, timedelta
import json


# select most complex model: nTypes, nFields
#model_name = ""
#for model_name0 in dictModelStructure:
#	model_name = model_name0
#	break


listModels = []
for (model_name, model_def) in dictModelStructure.items():

#	setTypes = Set()
#	for field_def in model_def['fields']:
#		setTypes.add( field_def['type'] )
	setTypes = { field_def['type'] for field_def in model_def['fields'] }

	listModels.append ( {
		'model_name': model_name, 
		'nTypes': len(setTypes), 
		'nFields': len( model_def['fields'] ), 
		} )

el_model = max( listModels, key=lambda obj: obj['nTypes']*1000 + obj['nFields'] )

try:
	model_name = el_model['model_name']

#	print ('selected model: ' + model_name )
except:
	pass


def create_dictTestRowValues(_model_name): 
	dictTypeTestValues = {
		'int': 117,
		'char': "test string",
#		'date': datetime.today()
		'date': datetime.today().date()
	}

	listFields = dictModelStructure[ _model_name ]['fields'] 

	dictValues = {}
	for field_def in listFields:
		if field_def['id'] == 'id':
			continue
		dictValues[ field_def['id'] ] = dictTypeTestValues[field_def['type']]

	return dictValues

def create_dictTestRowValuesNew(_model_name): 
	dictTypeTestValues = {
		'int': 203,
		'char': "test string new",
#		'date': datetime.today()
		'date': datetime.today().date() + timedelta(10)
	}

	listFields = dictModelStructure[ _model_name ]['fields'] 

	dictValues = {}
	for field_def in listFields:
		if field_def['id'] == 'id':
			continue
		dictValues[ field_def['id'] ] = dictTypeTestValues[field_def['type']]

	return dictValues

#def create_db_row( _model_name ):
#
#	dictValues = create_dictTestRowValues( model_name )
#	Model = dictModelClasses[ _model_name ]
#
#	obj = Model( **dictValues )
#	obj.save()

#?
class AllModels(TestCase):

	def test_not_empty(self):
		self.assertEqual( 0 < len(dictModelClasses), True )


class OneModel(TestCase):

	def test_create_instance(self):
		def one_model_test( model_name ):
			dictValues = create_dictTestRowValues( model_name )
			Model = dictModelClasses[ model_name ]

			isCtreated = False
			try:
				obj = Model( **dictValues )
				isCtreated = True
			except:
				print ('Error, create model ' + model_name  )


			self.assertEqual( isCtreated, True )


		for model_name in dictModelStructure:
			one_model_test( model_name )


	def test_create_instance_fields(self):
		def one_model_test( model_name ):
			isError = False

			dictValues = create_dictTestRowValues( model_name );
			Model = dictModelClasses[ model_name ]

			obj = Model( **dictValues )


			for (field_name, test_value) in dictValues.items():
				obj_value = getattr( obj, field_name )
				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' + str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        


		for model_name in dictModelStructure:
			one_model_test( model_name )


	def test_save_row(self):
		def one_model_test( model_name ):

			dictValues = create_dictTestRowValues( model_name );
			Model = dictModelClasses[ model_name ]

			obj = Model( **dictValues )
			obj.save()

			list_obj = Model.objects.all()

			self.assertEqual( len(list_obj), 1 )        
			obj = list_obj[0]

			isError = False
			for (field_name, test_value) in dictValues.items():
				obj_value = getattr( obj, field_name )
				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' + str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        

		for model_name in dictModelStructure:
			one_model_test( model_name )


class ViewTest_Index(TestCase):

	def test_get(self):
		def one_model_test( model_name ):
			response = self.client.get(reverse('index'))

	#		print(response)

			self.assertEqual( response.status_code, 200 )
	#		self.assertContains(response, "No polls are available.")
			self.assertEqual( len(response.context['dmodels_list']), len(dictModelClasses) )

		for model_name in dictModelStructure:
			one_model_test( model_name )


class ViewTest_ajax_get_list(TestCase):

	def test_get(self):
		def one_model_test( model_name ):

			listFields = dictModelStructure[ model_name ]['fields'] 

	#		response = self.client.get( reverse('dmodels.views.ajax_get_list', args=(model_name,) ) )
			response = self.client.get( reverse('ajax_get_list', args=(model_name,) ) )

	#		print(dir(response))
	#		print(response.content)
			obj_json = json.loads( response.content )

			self.assertEqual( response.status_code, 200 )
			self.assertEqual( isinstance( obj_json, dict ), True )

			self.assertEqual( obj_json['model'], model_name )
			self.assertEqual( obj_json['fields'], listFields )
			self.assertEqual( isinstance( obj_json['data'], list ), True )
			self.assertEqual( len( obj_json['data'] ), 0 )


		for model_name in dictModelStructure:
			one_model_test( model_name )


	def test_get_add_fields(self):
		def one_model_test( model_name ):

	#		create_db_row( model_name )
			dictFields = dictModelStructure[ model_name ]['dictFilds'] 
			dictValues = create_dictTestRowValues( model_name )
			Model = dictModelClasses[ model_name ]

			obj = Model( **dictValues )
			obj.save()


			response = self.client.get( reverse('ajax_get_list', args=(model_name,) ) )
			obj_json = json.loads( response.content )

			self.assertEqual( len( obj_json['data'] ), 1 )

			data = obj_json['data']
			row = data[0]
			self.assertEqual( isinstance( row, list ), True )



			isError = False
			for (field_name, test_value) in dictValues.items():
				field_def = dictFields[field_name]
				obj_value = row[ field_def['i_field'] ]

				if (field_def['type'] == 'date'):
					obj_value = datetime.strptime( obj_value, '%m/%d/%Y' ).date()

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' + str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        


		for model_name in dictModelStructure:
			one_model_test( model_name )


class ViewTest_ajax_add(TestCase):

	def test_add_db(self):
		def one_model_test( model_name ):

			dictFields = dictModelStructure[ model_name ]['dictFilds'] 


			dictValues = create_dictTestRowValues( model_name )

			dictValuesFormat = {}
			for (field_name, test_value) in dictValues.items():
				field_def = dictFields[field_name]

				new_value = test_value
				if field_def['type'] == 'date':
					new_value = test_value.strftime( '%m/%d/%Y' )
				dictValuesFormat[field_name] = new_value


#			listParams = [''+field_name+'='+str(value) for (field_name, value ) in  dictValuesFormat.items()]
#
#			strHref = reverse('ajax_add', args=(model_name,) )
#			strHref = strHref + '?' + '&'.join(listParams)
#
#	#		print(strHref)
#			response = self.client.get( strHref )

#			strHref = 'ajax_add/' + model_name 
			strHref = reverse('ajax_add', args=(model_name,) )
			response = self.client.post( strHref, dictValuesFormat )


			Model = dictModelClasses[ model_name ]
			list_obj = Model.objects.all()
			self.assertEqual( len(list_obj), 1 )

			obj = list_obj[0]
			isError = False
			for (field_name, test_value) in dictValues.items():
	#			field_def = dictFields[field_name]

				obj_value = getattr( obj, field_name )

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' + str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        


		for model_name in dictModelStructure:
			one_model_test( model_name )


	def test_add_response(self):
		def one_model_test( model_name ):

			dictFields = dictModelStructure[ model_name ]['dictFilds'] 


			dictValues = create_dictTestRowValues( model_name )

			dictValuesFormat = {}
			for (field_name, test_value) in dictValues.items():
				field_def = dictFields[field_name]

				new_value = test_value
				if field_def['type'] == 'date':
					new_value = test_value.strftime( '%m/%d/%Y' )
				dictValuesFormat[field_name] = new_value

#			listParams = [''+field_name+'='+str(value) for (field_name, value ) in  dictValuesFormat.items()]
#
#
#			strHref = reverse('ajax_add', args=(model_name,) )
#			strHref = strHref + '?' + '&'.join(listParams)
#
#	#		print(strHref)
#			response = self.client.get( strHref )

#			strHref = 'ajax_add/' + model_name 
			strHref = reverse('ajax_add', args=(model_name,) )
			response = self.client.post( strHref, dictValuesFormat )

			self.assertEqual( response.status_code, 200 )


			obj_json = json.loads( response.content )
			self.assertEqual( isinstance( obj_json, dict ), True )

			self.assertEqual( obj_json['model'], model_name )
			self.assertEqual( isinstance(obj_json['data'], list), True )
			self.assertEqual( len(obj_json['data']), 1 )

			row = obj_json['data'][0]
			row_id = row[ dictFields['id']['i_field'] ]
			self.assertEqual( 0 < row_id , True )


			isError = False
			for (field_name, test_value) in dictValues.items():
				field_def = dictFields[field_name]

				obj_value = row[ field_def['i_field'] ]

				if (field_def['type'] == 'date'):
					test_value = datetime.strftime( test_value, '%m/%d/%Y' )
				if (field_def['type'] == 'int'):
					test_value = str(test_value)

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' + str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        


		for model_name in dictModelStructure:
			one_model_test( model_name )


class ViewTest_ajax_change(TestCase):

	def test_change_db(self):
		def one_model_test( model_name ):

			# before: create row, _row_id
	#		dictValues = create_dictTestRowValues( model_name );
			Model = dictModelClasses[ model_name ]
			dictFields = dictModelStructure[ model_name ]['dictFilds'] 


			dictValues = create_dictTestRowValues( model_name )
			obj = Model( **dictValues )
			obj.save()

			list_obj = Model.objects.all()

			self.assertEqual( len(list_obj), 1 )        
			obj = list_obj[0]
			_row_id = getattr( obj, 'id')


			#action
			dictNewValues = create_dictTestRowValuesNew( model_name );
			dictValuesFormat = {}
			for (field_name, value ) in dictNewValues.items():
				new_value = value
				if dictFields[field_name]['type'] == 'date':
					new_value = value.strftime( '%m/%d/%Y' )
				dictValuesFormat[field_name] = new_value

#			listParams = [''+field_name+'='+str(value) for (field_name, value) in  dictValuesFormat.items()]


#			strHref = reverse('ajax_change', args=(model_name, _row_id) )
#			strHref = strHref + '?' + '&'.join(listParams)
#			response = self.client.get( strHref )

			strHref = reverse('ajax_change', args=(model_name, _row_id) )
			response = self.client.post( strHref, dictValuesFormat )


			#result
			list_obj = Model.objects.all()
			self.assertEqual( len(list_obj), 1 )

			obj = Model.objects.get( **{'id': _row_id} )

			isError = False
			for (field_name, test_value) in dictNewValues.items():
	#			field_def = dictFields[field_name]

				obj_value = getattr( obj, field_name )

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' + str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        


		for model_name in dictModelStructure:
			one_model_test( model_name )


	def test_change_response(self):
		def one_model_test( model_name ):

			# before: create row, _row_id
			Model = dictModelClasses[ model_name ]
			dictFields = dictModelStructure[ model_name ]['dictFilds'] 


			dictValues = create_dictTestRowValues( model_name )
			obj = Model( **dictValues )
			obj.save()

			list_obj = Model.objects.all()

			self.assertEqual( len(list_obj), 1 )        
			obj = list_obj[0]
			_row_id = getattr( obj, 'id')


			#action
			dictNewValues = create_dictTestRowValuesNew( model_name );
			dictValuesFormat = {}
			for (field_name, value ) in dictNewValues.items():
				new_value = value
				if dictFields[field_name]['type'] == 'date':
					new_value = value.strftime( '%m/%d/%Y' )
				dictValuesFormat[field_name] = new_value

			listParams = [''+field_name+'='+str(value) for (field_name, value) in  dictValuesFormat.items()]


#			strHref = reverse('ajax_change', args=(model_name, _row_id) )
#			strHref = strHref + '?' + '&'.join(listParams)
#			response = self.client.get( strHref )

			strHref = reverse('ajax_change', args=(model_name, _row_id) )
			response = self.client.post( strHref, dictValuesFormat )


			self.assertEqual( response.status_code, 200 )


		for model_name in dictModelStructure:
			one_model_test( model_name )

