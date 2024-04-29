for i in range(0,4):
    print(i)
# 0
# 1
# 2
# 3

for i ,j in zip(range(3),range(1,4)):
    print(i,j)
# 0 1
# 1 2
# 2 3

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


for _ in range(3):
    print(1) 
# 1
# 1
# 1


for i,j in enumerate([10,20]):
    print(i,j)
# 0 10
# 1 20

from itertools import product
for i, j in product([0,1], [0,1,2]):
    print(i,j)
# 0 0
# 0 1
# 0 2
# 1 0
# 1 1
# 1 2

for i in range(65, 91):
    print(chr(i))
# A
# B
# C


for a, b in enumerate(["a","b","c"]):
    print(a,b)
# 0 a
# 1 b
# 2 c


A = ["a","b"]
B = ["c","d"]
[x+y for x in A for y in B]
# ['ac', 'ad', 'bc', 'bd']


from itertools import combinations
L = [1, 2, 3]
for combo in combinations(L, 2):
    print('('+str(combo[0]), str(combo[1])+')')
# (1 2)
# (1 3)
# (2 3)
