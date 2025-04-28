import matplotlib.pyplot as plt
import numpy as np

h =1
rho_b = 1
mu_b = 1
rho_a = 1
mu_a = 100

x = np.linspace(0, h, 100)

u_1 = (rho_b  * h * x) / (3 * mu_b)  -  (rho_a  * x) / (2 * mu_a) * (x-h/3)
u_2 = - rho_b * x / (2 * mu_b) * (x - h)

plt.plot(x, u_1, label='u_1')
plt.plot(x, u_2, label='u_2')

plt.legend()

plt.figure()
plt.plot(x, mu_a * np.gradient(u_1, x), label='du_1/dx')
plt.plot(x, mu_b * np.gradient(u_2, x), label='du_2/dx')
plt.legend()
plt.show()
