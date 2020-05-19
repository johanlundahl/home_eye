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
			return self._value.strftime('%-d %b %-H:%M')
		return str(self._value)
	
	@property
	def unit(self):
		if self.isnumber() and self.need_unit_prefix():
			factor, prefix = self.get_prefix()
			return prefix + self._unit
		return self._unit

	def isnumber(self):
		return isinstance(self._value, (int, float))

	def need_unit_prefix(self):
		return self._value >= 1000 and self._unit is not ''

	def get_prefix(self):
		if self._value >= 10**6:
			return (10**6, 'M')
		elif self._value >= 10**3:
			return (10**3, 'k')
		else:
			return (1, '')

	def format_number(self, value):
		if self.isnumber() and self.need_unit_prefix():
			factor, prefix = self.get_prefix()
			value = value / factor
		value = self.round(value)
		return value

	def round(self, value):
		return int(round(value, 0))

	def __str__(self):
		return '{} {}'.format(self.display_value, self.unit)

