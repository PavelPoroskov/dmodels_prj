import os
import sys
from datetime import datetime

from django.db import models
from django.conf import settings

import yaml


dictModelStructure = {}

str__module__ = os.path.split( os.path.dirname(__file__) )[-1]
str__module__ = str__module__ + '.models'

file_path = settings.DMODELS_SCHEME_YAMLFILE 
stream = file( file_path, 'r' )
dictTableDef = yaml.load(stream)

def get_fnUnicode( inFields ):
	fn__unicode__ = lambda _field_id: (
	    lambda _self: getattr( _self, _field_id )
	)
 	for dictOneField in inFields:
 		if dictOneField['type'] == 'char':
			return fn__unicode__( dictOneField['id'] )


for (table_name, table_def) in dictTableDef.iteritems():

	dictForClassX = dict()

	listFields = []
 	for dictOneField in table_def['fields']:
 		field_id = dictOneField['id'];
 		field_title = dictOneField['title'];
 		field_type = dictOneField['type'];

 		flagAdd = True
 		if field_type == 'char':
 			dictForClassX[field_id] = models.CharField( field_title, max_length=30 )
 		elif field_type == 'int':
 			dictForClassX[field_id] = models.IntegerField( field_title )
 		elif field_type == 'date':
# 			dictForClassX[field_id] = models.DateField( field_title )
			_field_id = "_" + field_id
 			dictForClassX[_field_id] = models.DateField( field_title, db_column=field_id )
 			dictForClassX[field_id] = property( lambda self: getattr( self, _field_id ).strftime( '%m/%d/%Y' ) , 
 				lambda self, newv: setattr( self, _field_id, datetime.strptime( newv, '%m/%d/%Y') ) )
 		else:
	 		flagAdd = False
 			pass

 		if flagAdd:
 			listFields.append( { 
 				'id' : field_id,
 				'title' : field_title,
 				'type' : field_type,
 			 } )
 		
	table_title = table_def['title']
	dictMeta = {
		'__module__': str__module__,
		'verbose_name': table_title,			
		'verbose_name_plural': table_title,			
	}

	dictForClassX['Meta'] = type( 'Meta', (), dictMeta )
	dictForClassX['__module__'] = str__module__
	dictForClassX['__unicode__'] = get_fnUnicode( table_def['fields'] )


	setattr( sys.modules[__name__], table_name, type( table_name, (models.Model,), dictForClassX) )

	listFields.insert( 0, { 
		'id' : 'id',
		'title' : 'id',
		'type' : 'int',
	 } )
	dictFilds = { f['id']: { 'title': f['title'], 'type': f['type'], 'i_field': i } for (i, f) in enumerate(listFields) }

	dictModelStructure[table_name] = { 
#		'table_name': table_name,
		'table_title': table_title,
		'fields': listFields, 
		'dictFilds': dictFilds, 
	} 

	
