

from home_eye.model.value import Value
from datetime import datetime

bv = Value(1234567890, 'b')

print(bv)
print(str(bv))
print(bv.display_value, bv.unit)


bv = Value(123, 'b')
print(bv)

bv = Value(1234, 'b')
print(bv)

bv = Value(12345, 'b')
print(bv)

bv = Value(123456, 'b')
print(bv)

bv = Value(1234567, 'b')
print(bv)
