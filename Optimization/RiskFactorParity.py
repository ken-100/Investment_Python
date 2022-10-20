import pandas as pd
import numpy as np
import scipy.optimize as sco
from numpy import linalg
# https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.optimize.minimize.html
# https://quantu.hateblo.jp/entry/2017/12/27/010526

Cov = pd.DataFrame(np.zeros([4,4]))
Cov.loc[0,:]=[0.0449016,0.0396086,0.0442209,0.0323200]
Cov.loc[1,:]=[0.0396086,0.0733868,0.0543290,0.0357016]
Cov.loc[2,:]=[0.0442209,0.0543290,0.0689063,0.0400982]
Cov.loc[3,:]=[0.0323200,0.0357016,0.0400982,0.0530842]

#FactorParity
from scipy.linalg import null_space
A = pd.DataFrame(np.zeros([4,3]))
A.loc[0,:]=[0.9,0,0.5]
A.loc[1,:]=[1.1,0.5,0]
A.loc[2,:]=[1.2,0.3,0.2]
A.loc[3,:]=[0.8,0.1,0.7]
pinvA = np.linalg.pinv(A)
pinvB = np.linalg.pinv(A.T)
pinvB_NS = null_space(pinvB.T)
pinvB_NS *= np.sign(pinvB_NS[0,0])
B_Bar = np.c_[pinvB, pinvB_NS]

B_Tilde = np.linalg.inv(B_Bar)[len(B)-1,:]

# x=[0.25,0.25,0.25,0.25]
# SD = np.dot(np.dot(np.array(x),Cov),np.array(x).T)**0.5
# RC_F = np.dot(A.T,x) * np.dot(np.dot(pinvA ,Cov),x) / SD
# RC_Tilde_F = np.dot(B_Tilde,x) * np.dot(np.dot(B_Tilde ,Cov),x) / SD

def f(w):
    SD = np.dot(np.dot(np.array(w),Cov),np.array(w).T)**0.5
    RC_F = np.dot(A.T,w) * np.dot(np.dot(pinvA ,Cov),w) / SD
    RC_Tilde_F = np.dot(B_Tilde,w) * np.dot(np.dot(B_Tilde ,Cov),w) / SD
    return sum( (RC_F / SD - 1/len(RC_F))**2 ) 

B= [(0.001, 1)] * len(Cov)
C = [{'type': 'eq', 'fun': lambda w: sum(w) - 1}]
w0 =[1. / len(Cov)] * len(Cov)

opts = sco.minimize(fun=f, x0=w0, method='SLSQP', bounds=B, constraints=C)


ww = opts["x"]
SD = np.dot(np.dot(np.array(ww),Cov),np.array(ww).T)**0.5

tmp = ["Weight","SD","W*SD","RC","RC%"]
Summary = pd.DataFrame(np.zeros([len(tmp),len(Cov)]),index=tmp)
Summary.loc["Weight",:] = ww
Summary.loc["SD",:] = SD0
Summary.loc["W*SD",:] = ww * SD0
Summary.loc["RC",:] = RC
Summary.loc["RC%",:] = RC/SD

for i in range(0,len(Summary)):
    Summary.loc[Summary.index[i],"Net"] = sum( Summary.loc[Summary.index[i],list(range(0,len(Cov)))] )
    Summary.iloc[i,:] = Summary.iloc[i,:].apply("{:.1%}".format)

Summary.loc["SD","Net"] = "-"

RC_F = np.dot(A.T,ww) * np.dot(np.dot(pinvA ,Cov),ww) / SD
RC_Tilde_F = np.dot(B_Tilde,ww) * np.dot(np.dot(B_Tilde ,Cov),ww) / SD
sum(RC_F,RC_Tilde_F)


print("Port byAsset")
Summary



tmp = ["RC"]
Summary2 = pd.DataFrame(np.zeros([len(tmp),len(Cov)]), index=tmp, columns=list(range(0,len(Cov)-1)) + ["Additional"])
Summary2.loc["RC",:] = list(RC_F) + [RC_Tilde_F]
Summary2.loc["RC","Net"] = sum(Summary2.loc["RC",:])

Summary2.iloc[0,:] = Summary2.iloc[0,:].apply("{:.2%}".format)
print("SD_byFactor:")
Summary2
