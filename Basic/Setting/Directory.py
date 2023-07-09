import os
os.getcwd()

path = r"C:\Users"     #ex) C:/Users/
path = path.replace("\\", "/")
os.chdir(path)
print(os.getcwd())
# C:\Users


from pathlib import Path
Path.cwd()
