from django.db import models

fields = models.fields;

dictStrTypeToField = {
	"int":  { 'Field': fields.IntegerField, 'kwargs': {} },
	"char": { 'Field': fields.CharField, 'kwargs': { 'max_length': 30 } },
	"date": { 'Field': fields.DateField, 'kwargs': {} },
}

dictFieldToStrType = { value['Field']: key for key, value in dictStrTypeToField.items() }
dictFieldToStrType[fields.AutoField] = "int"

