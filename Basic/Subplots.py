import numpy as np
import matplotlib.pyplot as plt


# Color
# https://matplotlib.org/stable/gallery/color/named_colors.html

#https://www.yutaka-note.com/entry/matplotlib_subplots

x = np.linspace(-3,3)
y1 = x**2
y2 = x
fig, ax = plt.subplots(1, 2, squeeze=False,figsize=(8,3),tight_layout=True)
ax[0,0].plot(x, y1,"SteelBlue", linewidth=2)
ax[0,0].plot(x, y2,"LightSteelBlue")
ax[0,0].set_title("A")
ax[0,0].legend(["test1","test2"])

ax[0,1].plot(x, y2)
ax[0,1].set_title("B")
ax[0,1].legend(["test2"])
ax[0,1].set_xticks(list(range(-3,8,2)))

fig.autofmt_xdate()
plt.show()
