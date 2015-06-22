
from django.core import exceptions
from django.db.models.fields import IntegerField as djIntegerField
#import sys

class IntegerField(djIntegerField):
	def to_python(self, value):
		print ('to_python')
		if value is None:
			return value
		try:
			return int(value)
		except UnicodeEncodeError:
			msg = self.error_messages['invalid'] % value
			raise exceptions.ValidationError(msg)
		except (TypeError, ValueError):
			msg = self.error_messages['invalid'] % str(value)
			raise exceptions.ValidationError(msg)

