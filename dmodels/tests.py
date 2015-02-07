from datetime import datetime, timedelta
import json


from django.test import TestCase
from django.core.urlresolvers import reverse


from dmodels import models
from dmodels import engine

def create_dictTestRowValues(_Model,from_client=False): 
	dictTypeTestValues = {
		'int': 117,
		'char': "test string",
#		'date': datetime.today()
		'date': datetime.today().date()
#		'date': "09/01/2014"
	}

	if from_client:
		dictTypeTestValues['date'] = dictTypeTestValues['date'].strftime( '%m/%d/%Y' )

	listFields = engine.getFields(_Model)

	dictValues = {}
	for field_def in listFields:
		if field_def['id'] == 'id':
			continue
		dictValues[ field_def['id'] ] = dictTypeTestValues[field_def['type']]

	return dictValues

def create_dictTestRowValuesNew(_Model,from_client=False): 
	dictTypeTestValues = {
		'int': 203,
		'char': "test string new",
#		'date': datetime.today()
		'date': datetime.today().date() + timedelta(10)
#		'date': "09/11/2014"
	}

	if from_client:
		dictTypeTestValues['date'] = dictTypeTestValues['date'].strftime( '%m/%d/%Y' )

	listFields = engine.getFields(_Model)

	dictValues = {}
	for field_def in listFields:
		if field_def['id'] == 'id':
			continue
		dictValues[ field_def['id'] ] = dictTypeTestValues[field_def['type']]

	return dictValues


class AllModels(TestCase):

	def test_not_empty(self):
		listModels = engine.getModels(models)
		self.assertEqual( 0 < len(listModels), True )


class OneModel(TestCase):

	def test_save_row(self):
		def one_model_test( _ModelInfo ):
			Model = _ModelInfo['model']
			model_name = _ModelInfo['table_name']

			dictTestValues = create_dictTestRowValues( Model )

			obj = Model( **dictTestValues )
			obj.save()

			list_obj = Model.objects.all()

			self.assertEqual( len(list_obj), 1 )        
			obj = list_obj[0]

			isError = False
			for (field_name, test_value) in dictTestValues.items():
				obj_value = getattr( obj, field_name )
				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' + str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        


		listModels = engine.getModels(models)
		for model_info in listModels:
			one_model_test( model_info )


class ViewTest_Index(TestCase):

	def test_get(self):

		listModels = engine.getModels(models)
		response = self.client.get(reverse('index'))

		self.assertEqual( response.status_code, 200 )
		self.assertEqual( len(response.context['dmodels_list']), len(listModels) )



class ViewTest_ajax_get_list(TestCase):

	def test_ajax_get_list(self):
		def one_model_test( _ModelInfo ):
			Model = _ModelInfo['model']
			model_name = _ModelInfo['table_name']

			dictTestValues = create_dictTestRowValues( Model )

			#prepare
			listFieldInfo = engine.getFields(Model)
			dictFields = { finfo['id']: {'iCol': iCol, 'type': finfo['type'] } 
				for iCol, finfo in enumerate(listFieldInfo) }

			obj = Model( **dictTestValues )
			obj.save()

			#action
			response = self.client.get( reverse('ajax_get_list', args=(model_name,) ) )
			obj_json = json.loads( response.content )

			self.assertEqual( response.status_code, 200 )
			self.assertEqual( isinstance( obj_json, dict ), True )

			self.assertEqual( obj_json['model'], model_name )
			self.assertEqual( obj_json['fields'], listFieldInfo )
			self.assertEqual( isinstance( obj_json['data'], list ), True )

			self.assertEqual( len( obj_json['data'] ), 1 )

			data = obj_json['data']
			row = data[0]
			self.assertEqual( isinstance( row, list ), True )


			dictTestValuesFromClient = create_dictTestRowValues( Model, from_client=True )

			isError = False
			for (field_name, test_value) in dictTestValuesFromClient.items():
				obj_value = row[ dictFields[field_name]['iCol'] ]

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' 
						+ str(obj_value) + ' != ' + str(test_value) )
					isError = True

			self.assertEqual( isError, False )        


		listModels = engine.getModels(models)
		for model_info in listModels:
			one_model_test( model_info )


class ViewTest_ajax_add(TestCase):

	def test_ajax_add(self):
		def one_model_test( _ModelInfo ):
			Model = _ModelInfo['model']
			model_name = _ModelInfo['table_name']

			listFieldInfo = engine.getFields(Model)
			dictFields = { finfo['id']: {'iCol': iCol, 'type': finfo['type'] } 
				for iCol, finfo in enumerate(listFieldInfo) }

			dictTestValues = create_dictTestRowValues( Model, from_client=False )
			dictTestValuesFromClient = create_dictTestRowValues( Model, from_client=True )


			strHref = reverse('ajax_add', args=(model_name,) )
			response = self.client.post( strHref, dictTestValuesFromClient )


			# responce to client
			self.assertEqual( response.status_code, 200 )


			obj_json = json.loads( response.content )
			self.assertEqual( isinstance( obj_json, dict ), True )

			self.assertEqual( obj_json['model'], model_name )
			self.assertEqual( isinstance(obj_json['data'], list), True )
			self.assertEqual( len(obj_json['data']), 1 )

			row = obj_json['data'][0]
			row_id = row[ dictFields['id']['iCol'] ]
			self.assertEqual( 0 < row_id , True )


			isResponceError = False
			for (field_name, test_value) in dictTestValuesFromClient.items():
				obj_value = row[ dictFields[field_name]['iCol'] ]

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' 
						+ str(obj_value) + ' != ' + str(test_value) )
					isResponceError = True

			self.assertEqual( isResponceError, False )        


			# save in db
			list_obj = Model.objects.all()
			self.assertEqual( len(list_obj), 1 )

			obj = list_obj[0]
			isSaveError = False
			for (field_name, test_value) in dictTestValues.items():
				obj_value = getattr( obj, field_name )

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' 
						+ str(obj_value) + ' != ' + str(test_value) )
					isSaveError = True

			self.assertEqual( isSaveError, False )        




		listModels = engine.getModels(models)
		for model_info in listModels:
			one_model_test( model_info )


class ViewTest_ajax_change(TestCase):

	def test_ajax_change(self):
		def one_model_test( _ModelInfo ):
			Model = _ModelInfo['model']
			model_name = _ModelInfo['table_name']

			#prepare
			dictTestValues =	 create_dictTestRowValues( Model )
			dictTestValues_NewFromClient = create_dictTestRowValuesNew( Model, from_client=True )
			dictTestValues_New = create_dictTestRowValuesNew( Model )

			obj = Model( **dictTestValues )
			obj.save()

			list_obj = Model.objects.all()

			self.assertEqual( len(list_obj), 1 )        
			obj = list_obj[0]
			_row_id = getattr( obj, 'id')


			#action

			strHref = reverse('ajax_change', args=(model_name, _row_id) )
			response = self.client.post( strHref, dictTestValues_NewFromClient )

			#responce to client
			self.assertEqual( response.status_code, 200 )

			#change in db
			list_obj = Model.objects.all()
			self.assertEqual( len(list_obj), 1 )

			obj = Model.objects.get( **{'id': _row_id} )

			isSaveError = False
			for (field_name, test_value) in dictTestValues_New.items():

				obj_value = getattr( obj, field_name )

				if obj_value != test_value:
					print (' model (field): ' + model_name + '(' + field_name + ') ' 
						+ str(obj_value) + ' != ' + str(test_value) )
					isSaveError = True

			self.assertEqual( isSaveError, False )        



		listModels = engine.getModels(models)
		for model_info in listModels:
			one_model_test( model_info )
