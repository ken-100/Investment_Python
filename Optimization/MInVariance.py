import pandas as pd
import numpy as np
import scipy.optimize as sco
from numpy import linalg
# https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.optimize.minimize.html

# COBYLA
# slower than SLSQP
# more stable with respect to obtaining a solution than SLSQP
# cannot use bounds
# only inequality can be used as a constraint, not equality
# https://org-technology.com/posts/scipy-constrained-minimization-of-multivariate-scalar-functions.html#
# https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.optimize.minimize.html

Cov = pd.DataFrame(np.zeros([4,4]))
Cov.loc[0,:]=[0.0449016,0.0396086,0.0442209,0.0323200]
Cov.loc[1,:]=[0.0396086,0.0733868,0.0543290,0.0357016]
Cov.loc[2,:]=[0.0442209,0.0543290,0.0689063,0.0400982]
Cov.loc[3,:]=[0.0323200,0.0357016,0.0400982,0.0530842]

def f(w):
    SD = np.dot(np.dot(np.array(w),Cov),np.array(w).T)**0.5
    return SD 

def opts(m,C):
    SD0 = np.diag(Cov**0.5)
    tmp = 1/SD0   
    w0 = tmp/sum(tmp)

    if m == "SLSQP":
        B= [(0, 1)] * len(Cov)
        opts = sco.minimize(fun=f, x0=w0, method=m, bounds=B, constraints=C)
    else:
        opts = sco.minimize(fun=f, x0=w0, method=m, constraints=C)

    ww = opts["x"]
    SD = np.dot(np.dot(np.array(ww),Cov),np.array(ww).T)**0.5
    RC = ww * (np.dot(np.array(ww),Cov)) / SD

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
    return Summary
    
    
m = "SLSQP"  #Method
C = [{"type": "eq", "fun": lambda w: sum(w) - 1}]
Summary = opts(m,C)

print("MinVariance")
Summary


m = "COBYLA"  #Method
c0 = {"type": "ineq", "fun": lambda w: -sum(w) + 1-0.0001}
c1 = {"type": "ineq", "fun": lambda w: sum(w) - 1.000}
c2 = {"type": "ineq", "fun": lambda w:  min(w) - 0.0001 } #min(w) >= 0.001 
C = [c0, c1, c2 ]
Summary = opts(m,C)

print("MinVariance")
Summary
