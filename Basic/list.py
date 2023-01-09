arr = [23, 6, 22, 3, 38, 15]

# Number of matching elements
n = sum(x>10 for x in arr)
print(n)
n = sum(1 for x in arr if x>10)
print(n)
n = sum([1 for x in arr if x>10])
print(n)
n = len([1 for x in arr if x>10])
print(n)
# 4
# 4
# 4
# 4

# Sum of matching elements
n = sum(x for x in arr if x>10)
print(n)
# 98
