import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos

#tạo đồ thị y = x
# thiết kế cho dễ nhìn

x1 = np.linspace(-10, 10, 100)

a = x1**5
b = x1**100
c = (2*x1**2 + 4*x1 - 5)**3
d = (x1**2 + 2)**(5/4)

#điều kiện x = [0,360]
x = np.linspace(0, 360, 100)
f1 = 1 + 2 * np.sin(x) * np.cos(x) + np.cos(x) + np.sin(x)
f2 = 3*np.sin(x) + 2*np.cos(x)
f3 = 2*(np.sin(x) + np.cos(x)) + 2*np.sin(x)*np.cos(x) + 2
plt.ylim(-10, 10)  # Giới hạn trục y từ -100 đến 100
plt.plot(x1, a, linewidth=0.7,label='y = x^5')
plt.plot(x1, b,linewidth=0.7 ,label='y = x^100')
plt.plot(x1, c,linewidth=0.7 ,label='y = (2x^2 + 4x - 5)^3')
plt.plot(x1, d,linewidth=0.7, label='y = (x^2 + 1)^3')
plt.plot(x, f1,linewidth=1, label='y = 1 + sin(2x) + cos(x) + sin(x)')
plt.plot(x, f2,linewidth=1, label='y = 3sin(x) + 2cos(x)')
plt.plot(x, f3, linewidth=1,label='y = 2(sin(x) + cos(x)) + 2sin(x)cos(x) + 2')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Đồ thị hàm số')
plt.legend()
plt.grid()
plt.show()

