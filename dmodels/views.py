
from datetime import datetime
import json


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect


from dmodels.models import dictModelStructure
from dmodels import models


@ensure_csrf_cookie
def index(request):
	list_Models = [{ 'table_name': key, 'table_title': val['table_title'] } for (key,val) in dictModelStructure.items() ]
	list_Models = sorted( list_Models, key=lambda obj: obj['table_title'] )

	context = { 'dmodels_list': list_Models }
	return render( request, 'index.html', context )


def ajax_get_list(request, model_name):

	listFields = dictModelStructure[model_name]['fields'] 

	Model = getattr( models, model_name )
	list_rows = Model.objects.all()

	new_data = []
	for row in list_rows:
		new_row = []
		for field in listFields:
			field_id = field['id']
			value = getattr( row, field_id )

			new_row.append( value )
			
		new_data.append( new_row )


	res_str = json.dumps({
		'model': model_name,
		'fields': listFields,
		'data': new_data
		})
	
	return HttpResponse(res_str)

@require_POST
@csrf_protect
def ajax_change( request, model_name, row_id ):

#	obj = dictModelClasses[model_name].objects.get( **{'id': row_id} )
	Model = getattr( models, model_name )
	obj = Model.objects.get( **{'id': row_id} )

	for (field, value) in request.POST.items():
		setattr( obj, field, value )

	obj.save()

	return HttpResponse("Ok")


@require_POST
@csrf_protect
def ajax_add( request, model_name ):

#	dictValues = {}
#	for (field, value) in request.POST.items(): 
#		dictValues[field] = value;
#	dictValues = { field: value for (field, value) in request.POST.items() } 
	dictFilds = dictModelStructure[model_name]['dictFilds'] 
	dictValues = { field: int(value) if dictFilds[field]['type'] == 'int' else value for (field, value) in request.POST.items() } 

#	print(dictValues)

#	obj = dictModelClasses[model_name]( **dictValues )
	Model = getattr( models, model_name )
#	obj = Model( **request.POST )
	obj = Model( **dictValues )
	obj.save()


	listFields = dictModelStructure[model_name]['fields'] 
	new_row = []
	for field in listFields:
		field_id = field['id']
		value = getattr( obj, field_id )
		new_row.append( value )


	res_str = json.dumps({
		'model': model_name,
		'data': [new_row]
		})
#	print(new_row)
#	print(res_str)

	return HttpResponse(res_str)


# add, change with POST (csrf protect)
# innerHTML --> textContent (XSS protect)
# models: @property for type "date", get/set string