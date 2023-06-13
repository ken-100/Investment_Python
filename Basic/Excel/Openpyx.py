import openpyxl
import pandas as pd
import numpy as np


%cd C:\blp\data


    
r = ws.max_row + 1   
c = ws.max_column + 1

#Read 
pd.DataFrame(ws.values)



for r in ws.rows:
    print('----------------------------')
    for cell in r:
        print(cell.value)

        
for c in ws.columns:
    print('----------------------------')
    for cell in c:
        print(cell.value)
