from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect


from dmodels import models
from dmodels import readmodels
from dmodels import serialize


@ensure_csrf_cookie
def index(request):
	list_Models = [{ 
		'table_name': dictModelInfo['table_name'], 
		'table_title': dictModelInfo['table_title'] 
		} for dictModelInfo in readmodels.getModels(models) ]
	
	list_Models = sorted( list_Models, key=lambda obj: obj['table_title'] )

	context = { 'dmodels_list': list_Models }
	return render( request, 'index.html', context )


def ajax_get_list(request, model_name):

	Model = getattr( models, model_name )
	list_rows = Model.objects.all()

	res_str = serialize.serialize( list_rows, Model )
	
	return HttpResponse(res_str)

@require_POST
@csrf_protect
def ajax_change( request, model_name, row_id ):

	Model = getattr( models, model_name )
	dictValues = serialize.deserialize( request.POST, Model )

	obj = Model.objects.get( **{'id': row_id} )
	for (field, value) in dictValues.items():
		setattr( obj, field, value )

#... ??? validation
	obj.save()

	return HttpResponse("Ok")


@require_POST
@csrf_protect
def ajax_add( request, model_name ):

	Model = getattr( models, model_name )
	dictValues = serialize.deserialize( request.POST, Model )

	obj = Model( **dictValues )
#... ??? validation
	obj.save()

	res_str = serialize.serialize( obj, Model )

	return HttpResponse(res_str)


# add, change with POST (csrf protect)
# innerHTML --> textContent (XSS protect)
# models: @property for type "date", get/set string