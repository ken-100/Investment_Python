#https://qiita.com/AnchorBlues/items/883790e43417640140aa
import sys
print("{}{: >25}{}{: >10}{}".format('|','Variable Name','|','Memory','|'))
print(" ------------------------------------ ")
for var_name in dir():
    if not var_name.startswith("_") and sys.getsizeof(eval(var_name)) > 10000:
        print("{}{: >25}{}{: >10}{}".format('|',var_name,'|',str(round(sys.getsizeof(eval(var_name))/1024**2,1))+'MB','|'))
        
del A





# https://www.haya-programming.com/entry/2017/02/09/190512
L = [1,2]

# Use a lot of memory
tmp = [ x for x in L]

# Recommended
tmp = []
for x in L:
    tmp += [x]
