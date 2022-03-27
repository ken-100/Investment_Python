import pandas as pd
import numpy as np
import scipy.optimize as sco
# https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.optimize.minimize.html

from numpy import linalg

Cov = pd.DataFrame(np.zeros([4,4]))
Cov.loc[0,:]=[0.0449016,0.0396086,0.0442209,0.0323200]
Cov.loc[1,:]=[0.0396086,0.0733868,0.0543290,0.0357016]
Cov.loc[2,:]=[0.0442209,0.0543290,0.0689063,0.0400982]
Cov.loc[3,:]=[0.0323200,0.0357016,0.0400982,0.0530842]

def f(w):
    SD = np.dot(np.dot(np.array(w),Cov),np.array(w).T)**0.5
    return SD 

B = [(0.001, 1)] * len(Cov)
C = [{'type': 'eq', 'fun': lambda w: sum(w) - 1}]
w0 =[1. / len(Cov)] * len(Cov)

opts = sco.minimize(fun=f, x0=w0, method='SLSQP', bounds=B, constraints=C)

ww = opts["x"]
print("Weight:",ww,"Net:",sum(ww))
SD = np.dot(np.dot(np.array(ww),Cov),np.array(ww).T)**0.5
RC = ww * (np.dot(np.array(ww),Cov)) / SD
WA = sum(ww * np.diag(Cov**0.5))

print("SD:",SD)
print("RC:",RC)
print("Ret:",opts["fun"])
print("WA/SD:",WA/SD)
