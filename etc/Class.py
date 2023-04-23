# ex1
class SimpleData:

    a = 0
    b = 0
    
    def set(self, a, b):
        self.a = a
        self.b = b
        
    def sum(self):
        return self.a + self.b

data1 = SimpleData()
print(data1.sum())
data1.set(1, 2)
print(data1.sum())

# 0
# 3




# ex2
class SimpleData:
    
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def sum(self):
        return self.a + self.b

data1 = SimpleData(1,2)
print(data1.sum())

# 3
