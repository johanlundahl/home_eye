from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, '')

class Value:

	def __init__(self, value, unit=''):
		self._value = value
		self._unit = unit

	@property
	def value(self):
		return self._value
	
	@property
	def display_value(self):
		if isinstance(self._value, (int, float)):
			return '{0:n}'.format(self.format_number(self._value)) 
		if isinstance(self._value, str):
			return str(self._value.capitalize())
		if isinstance(self._value, datetime):
			return self._value.strftime('%-H:%M %-d %b')
		return str(self._value)
	
	@property
	def unit(self):
		return self._unit

	def format_number(self, value):
		value = self.thousand(value)
		value = self.round(value)
		return value

	def round(self, value):
		return int(round(value, 0))

	def thousand(self, value):
		if value > 999 and self._unit is not '':
			self._unit = 'k' + self._unit
			return value/1000
		else:
			return value

	def __str__(self):
		return '{} {}'.format(self.display_value, self.unit)