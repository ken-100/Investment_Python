!python --version
# Python 3.8.5


import numpy as np
print(np.__version__)
# 1.23.4

!pip show numpy
# Name: numpy
# Version: 1.23.4
# Summary: NumPy is the fundamental package for array computing with Python.


!pip install gym==0.26.2
import gym
print(gym.__version__)
# 0.26.2

!pip install gym==0.12.1
import gym
print(gym.__version__)
# 0.12.1

!pip list
# Package                            Version
# ---------------------------------- -------------------
# absl-py                            1.3.0
# alabaster                          0.7.12


!pip list | findstr xbbg
# xbbg                      1.2.2


!pip show xbbg
# Name: xbbg
# Version: 1.2.2
# Summary: Independent client for Bloomberg-connected data workflows
# Home-page: https://xbbg.org/
# Author: 
# Author-email: Alpha x1 <alpha.xone@outlook.com>
# License-Expression: Apache-2.0
# Location: C:\SMTAMSYS\Python313\Lib\site-packages
# Requires: narwhals
# Required-by: 
