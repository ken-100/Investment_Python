a = 7.123456789

print(round(a,2))
print(int(a))
print(str(a))
print(format(a, '.2f'))
print(format(a, '.0%'))
# 7.12
# 7
# 7.123456789
# 7.12
# 712%

import math
print(math.floor(a)) #Roundup
print(math.ceil(a)) #Rounddown
# 7
# 8
