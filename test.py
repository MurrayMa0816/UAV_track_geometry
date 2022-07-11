import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
 
x = np.array([2, 0.5,0.25, 0.1,  0.05,  0.02,  0.01, 0.005, 0.002])
y = np.array([75.70, 61.50, 41.30, 26.50, 16.00, 10.00, 5.90, 3.00, 0.00])
x_smooth = np.linspace(x.min(), x.max(), 300)  # np.linspace 等差数列,从x.min()到x.max()生成300个数，便于后续插值
# print(x)
y_smooth = make_interp_spline(x.sort(), y)(x_smooth)
plt.plot(x_smooth, y_smooth)
plt.show()