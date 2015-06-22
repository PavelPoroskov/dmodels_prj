import os
import sys
from operator import attrgetter

import yaml

from django.db import models

from dmodels import fieldrules



def loadFromYaml( _yaml_file, _to_module__name__ ):

	def get_fnUnicode( inFields ):
		fn__unicode__ = lambda _field_id: (
		    lambda _self: getattr( _self, _field_id )
#		    attrgetter( _field_id )
		)
	 	for dictOneField in inFields:
#	 		if dictOneField['type'] == 'char':
#				return fn__unicode__( dictOneField['id'] )
	 		if dictOneField['type'] in fieldrules.dictStrTypeToField:
		 		if fieldrules.dictStrTypeToField[ dictOneField['type'] ]['Field'] == models.fields.CharField:
					return fn__unicode__( dictOneField['id'] )
#					return attrgetter( dictOneField['id'] )
	

	stream = file( _yaml_file, 'r' )
	dictTableDef = yaml.load(stream)

	for (table_name, table_def) in dictTableDef.iteritems():

		dictForClassX = dict()

	 	for dictOneField in table_def['fields']:
	 		field_id = dictOneField['id'];
	 		field_title = dictOneField['title'];
	 		field_type = dictOneField['type'];

	 		if field_type in fieldrules.dictStrTypeToField:
	 			Field = fieldrules.dictStrTypeToField[field_type]['Field']
	 			kwargs = fieldrules.dictStrTypeToField[field_type]['kwargs']
	 			dictForClassX[field_id] = Field( field_title, **kwargs )

		table_title = table_def['title']
		dictMeta = {
			'__module__': _to_module__name__,
			'verbose_name': table_title,			
			'verbose_name_plural': table_title,			
		}

		dictForClassX['Meta'] = type( 'Meta', (), dictMeta )
		dictForClassX['__module__'] = _to_module__name__
		dictForClassX['__unicode__'] = get_fnUnicode( table_def['fields'] )


		setattr( sys.modules[_to_module__name__], table_name, type( table_name, (models.Model,), dictForClassX) )


	
