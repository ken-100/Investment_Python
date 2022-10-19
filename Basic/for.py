for i in range(0,4):
    print(i)
# 0
# 1
# 2
# 3

for i in range(0,4):
    if i==2:
        break
    print(i)
# 0
# 1

for i in range(0,4):
    if i==2:
        continue
    print(i)
# 0
# 1
# 3

for i in range(0,4,2):
    print(i)
# 0
# 2
    

  for i in range(4,0,-2):
    print(i)
# 4
# 2


for i in [10,20]:
    print(i)
# 10
# 20


for i,k in enumerate([10,20]):
    print(i,k)
# 0 10
# 1 20
