import openpyxl
import pandas as pd
import numpy as np


%cd C:\blp\data

tmp =  ["Name","Asset","Ticker","Ticker2","HC","Alt","Fx","Fx_R","Flag"]
T = pd.DataFrame(np.zeros([0,len(tmp)]),columns=tmp)


wb = openpyxl.load_workbook("為替FH.xlsx",data_only=True)['forPython']
for i in range(5,10):
    
    
    
    
        if wb["B"+str(i)].value is None:
            print(i)
            break
            
for row in wb["A4:E8"]:
    tmp = []
    for col in row:
        tmp.append(col.value)
    print(tmp)
    
pd.DataFrame(tmp)

