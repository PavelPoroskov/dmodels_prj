from django.db import models

#from dmodels.fix import IntegerField

fields = models.fields;

dictStrTypeToField = {
	"int":  { 'Field': fields.IntegerField, 'kwargs': {} },
#	"int":  { 'Field': IntegerField, 'kwargs': {} },
	"char": { 'Field': fields.CharField, 'kwargs': { 'max_length': 30 } },
	"date": { 'Field': fields.DateField, 'kwargs': {} },
}

dictFieldToStrType = { value['Field']: key for key, value in dictStrTypeToField.items() }
dictFieldToStrType[fields.AutoField] = "int"

