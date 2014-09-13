
from datetime import datetime
import json


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.db.models import Model as DjangoBaseModel


from dmodels.models import dictModelStructure
from dmodels import models

# data -- QueryView, obj
def serialize( data ):

	def object_to_arr( obj, listFields ):
		new_row = []
		for field in listFields:
			field_id = field['id']
			value = getattr( obj, field_id )

			new_row.append( value )

		return new_row


	model_name = ""
	isOneObj = False
	if issubclass( data.__class__, DjangoBaseModel ):
		isOneObj = True
		model_name = data.__class__.__name__
	else:  # QuerySet
		model_name = data.model.__name__
	Model = getattr( models, model_name )
	listFields = dictModelStructure[model_name]['fields'] 


	new_data = []
#	if isinstance( data, Model ):
	if isOneObj:
		new_row = object_to_arr( data, listFields )
		new_data.append( new_row )
	else: # QuerySet
		for row in data:
			new_row = object_to_arr( row, listFields )				
			new_data.append( new_row )


	res_str = json.dumps({
		'model': model_name,
		'fields': listFields,
		'data': new_data
		})

	return res_str

def deserialize( model_name, request_POST ):
	dictFilds = dictModelStructure[model_name]['dictFilds'] 
	dictValues = { field: int(value) if dictFilds[field]['type'] == 'int' else value 
					for (field, value) in request_POST.items() } 

	return dictValues


@ensure_csrf_cookie
def index(request):
	list_Models = [{ 'table_name': key, 'table_title': val['table_title'] } for (key,val) in dictModelStructure.items() ]
	list_Models = sorted( list_Models, key=lambda obj: obj['table_title'] )

	context = { 'dmodels_list': list_Models }
	return render( request, 'index.html', context )


def ajax_get_list(request, model_name):

	Model = getattr( models, model_name )
	list_rows = Model.objects.all()

	res_str = serialize( list_rows )
	
	return HttpResponse(res_str)

@require_POST
@csrf_protect
def ajax_change( request, model_name, row_id ):

	dictValues = deserialize( model_name, request.POST )

	Model = getattr( models, model_name )
	obj = Model.objects.get( **{'id': row_id} )
	for (field, value) in dictValues.items():
		setattr( obj, field, value )
	obj.save()

	return HttpResponse("Ok")


@require_POST
@csrf_protect
def ajax_add( request, model_name ):

	dictValues = deserialize( model_name, request.POST )

	Model = getattr( models, model_name )
	obj = Model( **dictValues )
	obj.save()

	res_str = serialize( obj )

	return HttpResponse(res_str)


# add, change with POST (csrf protect)
# innerHTML --> textContent (XSS protect)
# models: @property for type "date", get/set string