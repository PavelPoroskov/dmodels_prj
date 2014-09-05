from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

import json

from dmodels.models import dictModelStructure
from dmodels.models import dictModelClasses



list_Models = [{ 'table_name': key, 'table_title': val['table_title'] } for (key,val) in dictModelStructure.items() ];
list_Models = sorted( list_Models, key=lambda obj: obj['table_title'] );


@ensure_csrf_cookie
def index(request):
    context = { 'dmodels_list': list_Models }
    return render( request, 'index.html', context )

#for step-test
def detail(request, model_name):
	list_rows = dictModelClasses[model_name].objects.all()
	context = {'list_rows': list_rows}
	return render(request, 'index_m_test.html', context)	

def ajax_get_list(request, model_name):

	listFields = dictModelStructure[model_name]['fields'] 

	list_rows = dictModelClasses[model_name].objects.all()

# var 1	
	new_data = []
	for row in list_rows:
#		new_row = {}
		new_row = []
		for field in listFields:
#			new_row[field['id']] = row[field['id']]
			field_id = field['id']
			value = getattr( row, field_id )
			if field['type'] == 'date':
#				value = value.isoformat()
				value = value.strftime( '%m/%d/%Y' )

#			new_row[field_id] = value
			new_row.append( value )
			
		new_data.append( new_row )

## var 2
#	def makeRowWithFields( _listFields):
#		def makeRow( _old_row):
#			new_row = {}
#			for field in _listFields:
#	#			new_row[field['id']] = row[field['id']]
#				field_id = field['id']
#				value = getattr( _old_row, field_id )
#				if field['type'] == 'date':
#					value = value.isoformat()
#				new_row[field_id] = value
#
#			return new_row
#		return makeRow

#	fnMakeRow = makeRowWithFields( listFields )

##	new_data = []
##	for row in list_rows:
##		new_data.append( fnMakeRow(row) )

## var 2.2
#	new_data = [fnMakeRow(row) for row in list_rows]


#	res_str = json.dump({
	res_str = json.dumps({
		'model': model_name,
		'fields': listFields,
		'data': new_data
		})
	
	return HttpResponse(res_str)

# ?? security
@require_POST
@csrf_protect
def ajax_change( request, model_name, row_id ):

#	model_name = request.GET['model']
#	row_id = request.GET['row_id']

#	field_id = request.GET['field_id']
#	new_value = request.GET['new_value']
	dictFilds = dictModelStructure[model_name]['dictFilds'] 


	obj = dictModelClasses[model_name].objects.get( **{'id': row_id} )

#	for (field, value) in request.GET.items(): # 2014.09.03
	for (field, value) in request.POST.items():
		if dictFilds[field]['type'] == 'date':
			value = datetime.strptime( value, '%m/%d/%Y')
		setattr( obj, field, value )

	obj.save()

	return HttpResponse("Ok")

@require_POST
@csrf_protect
def ajax_add( request, model_name ):

	dictFilds = dictModelStructure[model_name]['dictFilds'] 

	dictValues = {};
#	for (field, value) in request.GET.items(): # 2014.09.03
	for (field, value) in request.POST.items(): 
		if dictFilds[field]['type'] == 'date':
			value = datetime.strptime( value, '%m/%d/%Y')
		dictValues[field] = value;

	obj = dictModelClasses[model_name]( **dictValues )
#	obj = dictClassModels[model_name]( **request.GET )
	obj.save()


	listFields = dictModelStructure[model_name]['fields'] 
	new_row = []
	for field in listFields:
#			new_row[field['id']] = row[field['id']]
		field_id = field['id']
		value = getattr( obj, field_id )
		if field['type'] == 'date':
#			value = value.isoformat()
			value = value.strftime( '%m/%d/%Y' )

#		new_row[field_id] = value
		new_row.append( value )


	res_str = json.dumps({
		'model': model_name,
		'data': [new_row]
		})

	return HttpResponse(res_str)


# add, change with POST
# innerHTML --+ textContent