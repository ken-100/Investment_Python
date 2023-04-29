# ex1
class SimpleData:

    a = 1
    b = 1
    
    def set(self, a, b):
        self.a = a
        self.b = b
        
    def sum(self):
        return self.a + self.b
    
    def multi(self):
        return self.a * self.b

data1 = SimpleData()
print(data1.sum())
print(data1.multi())

data1.set(1, 2)
print(data1.sum())
print(data1.multi())

# 2
# 1
# 3
# 2



# ex2
class SimpleData:
    
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def sum(self):
        return self.a + self.b
    
    def multi(self):
        return self.a * self.b

data1 = SimpleData(1,2)
print(data1.sum())
print(data1.multi())

# 3
# 2
