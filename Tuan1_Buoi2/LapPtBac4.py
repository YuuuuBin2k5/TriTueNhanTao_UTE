# Giải hệ và vẽ lát cắt 3D với w cố định
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Ma trận hệ số và vector kết quả
A = np.array([
	[2, 2, -1, 1],
	[4, 3, -1, 2],
	[8, 5, -3, 4],
	[3, 3, -2, 2]
])
B = np.array([4, 6, 12, 6])

# Giải hệ
solution = np.linalg.solve(A, B)
print("Nghiệm của hệ là:")
print(f"x = {solution[0]:.4f}")
print(f"y = {solution[1]:.4f}")
print(f"z = {solution[2]:.4f}")
print(f"w = {solution[3]:.4f}")

# Vẽ lát cắt 3D với w cố định
w = solution[3]  # dùng nghiệm thực tế
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Tính Z cho từng mặt phẳng với w cố định
Z1 = (4 - 2*X - 2*Y - w) / -1
Z2 = (6 - 4*X - 3*Y - 2*w) / -1
Z3 = (12 - 8*X - 5*Y - 4*w) / -3
Z4 = (6 - 3*X - 3*Y - 2*w) / -2

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z1, alpha=0.5, color='red', label='pt1')
ax.plot_surface(X, Y, Z2, alpha=0.5, color='green', label='pt2')
ax.plot_surface(X, Y, Z3, alpha=0.5, color='blue', label='pt3')
ax.plot_surface(X, Y, Z4, alpha=0.5, color='purple', label='pt4')

# Đánh dấu nghiệm trên lát cắt
ax.scatter(solution[0], solution[1], solution[2], color='black', s=100)
ax.text(solution[0], solution[1], solution[2], f'Nghiệm: (x={solution[0]:.2f}, y={solution[1]:.2f}, z={solution[2]:.2f}, w={solution[3]:.2f})', color='black')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title(f'Lát cắt 3D với w = {w:.2f} (nghiệm thực tế)')
plt.show()
