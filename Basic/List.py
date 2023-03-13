list(range(5))
# [0, 1, 2, 3, 4]


list(range(2,5))
# [2, 3, 4]


list(range(0,5,2))
# [0, 2, 4]


list(range(0,5,2)) * 2
# [0, 2, 4, 0, 2, 4]


tmp = list(range(0,5,2))
[x for x in tmp for y in range(2)]
# [0, 0, 2, 2, 4, 4]


list(range(5,0,-1))
# [5, 4, 3, 2, 1]


[i*0.1 for i in range(5)]
# [0.0, 0.1, 0.2, 0.3, 0.4]


A = ["a","b"]
B = ["c","d"]
tmp = [x+y for x in A for y in B]
print(tmp)
# ['ac', 'ad', 'bc', 'bd']

tmp.remove("ac")
print(tmp)
# ['ad', 'bc', 'bd']


np.zeros((3,4))
# array([[0., 0., 0., 0.],
#        [0., 0., 0., 0.],
#        [0., 0., 0., 0.]])
