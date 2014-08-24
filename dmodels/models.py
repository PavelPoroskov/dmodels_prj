from django.db import models
from django.conf import settings
import yaml
import os

dictModelClasses = {}
dictModelStructure = {}

str__module__ = os.path.split( os.path.dirname(__file__) )[-1]
str__module__ = str__module__ + '.models'

file_path = settings.DMODELS_SCHEME_YAMLFILE 
stream = file( file_path, 'r' )
dictTableDef = yaml.load(stream)


#class TestModel(models.Model):
#	test_field = models.IntegerField( )
#
#	class Meta:
#		verbose_name_plural = 'tra-ta-ta'

for (table_name, table_def) in dictTableDef.iteritems():

	dictForClassX = dict()

	listFields = []
	listFields.append( { 
		'id' : 'id',
		'title' : 'id',
		'type' : 'int',
	 } )
	dictFilds = {}
	i_field = 0
	dictFilds['id'] = { 
		'title' : 'id',
		'type' : int,
		'i_field': i_field,
	}
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
 			dictForClassX[field_id] = models.DateField( field_title )
 		else:
	 		flagAdd = False
 			pass

 		if flagAdd:
 			i_field = i_field + 1

 			listFields.append( { 
# 				'id' : field_title,
 				'id' : field_id,
 				'title' : field_title,
 				'type' : field_type,
 			 } )
 			dictFilds[field_id] = { 
 				'title' : field_title,
 				'type' : field_type,
 				'i_field': i_field,
 			}
 		
	table_title = table_def['title']
	dictMeta = {
		'__module__': str__module__,
		'verbose_name': table_title,			
		'verbose_name_plural': table_title,			
	}
	dictForClassX['Meta'] = type( 'Meta', (), dictMeta )
 
	dictForClassX['__module__'] = str__module__


	fn__unicode__ = lambda _field_id: (
	    lambda _self: getattr( _self, _field_id )
	)
 	for dictOneField in table_def['fields']:
 		if dictOneField['type'] == 'char':
			dictForClassX['__unicode__'] = fn__unicode__( dictOneField['id'] )


	dictModelClasses[table_name] = type( table_name, (models.Model,), dictForClassX )

	dictModelStructure[table_name] = { 
#		'table_name': table_name,
		'table_title': table_title,
		'fields': listFields, 
		'dictFilds': dictFilds, 
	} 

	