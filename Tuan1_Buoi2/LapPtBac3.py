# Vẽ mặt phẳng và đánh dấu nghiệm đúng
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)


# Tính Z cho từng mặt phẳng đúng hệ số
# Phương trình 1: 2x + 1y - 2z = 8
Z1 = (8 - 2*X - 1*Y) / -2
# Phương trình 2: 3x + 2y - 4z = 15
Z2 = (15 - 3*X - 2*Y) / -4
# Phương trình 3: 5x + 4y - z = 1
Z3 = 5*X + 4*Y - 1

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

# Vẽ mặt phẳng
ax.plot_surface(X, Y, Z1, alpha=0.5, color='red')
ax.plot_surface(X, Y, Z2, alpha=0.5, color='green')
ax.plot_surface(X, Y, Z3, alpha=0.5, color='blue')


# Đánh dấu nghiệm đúng
solution = np.linalg.solve([[2, 1, -2], [3, 2, -4], [5, 4, -1]], [8, 15, 1])
ax.scatter(solution[0], solution[1], solution[2], color='black', s=100)
ax.text(solution[0], solution[1], solution[2], f'Nghiệm: ({solution[0]:.2f}, {solution[1]:.2f}, {solution[2]:.2f})', color='black')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Mặt phẳng các phương trình và nghiệm giao điểm')
plt.show()