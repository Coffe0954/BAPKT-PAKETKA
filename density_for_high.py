import json
import matplotlib.pyplot as plt
from math import exp, log

# КОНСТАНТЫ
H_0 = 55 * 10 ** 3  # высота начала падения в метрах
R = 8.31  # универсальная газовая постоянная в Дж/(градус*моль)
M = 0.044  # молярная масса СО2 в кг/моль
g = 16.7  # ускорение свободного падения в м/с^2
p_0 = 6.517  # плотность воздуха на уровне моря кг/м^3

h_1 = 5000  # м
p_1 = 4.633  # кг/м^3
h_2 = 10000  # м
p_2 = 3.036  # кг/м^3

density_for_high = {}
H = (h_2 - h_1) / log(p_1 / p_2)

for high in range(56):
    density = p_0 * exp(-high * 1000 / H)
    density_for_high[high] = density

with open("flight_atmosphere_density (1).json", encoding="UTF-8") as file_in:
    ksp_data = json.load(file_in)

ksp_density = {}

for altitude, density in ksp_data.items():
    ksp_density[float(altitude) / 1000] = density


x_ksp = list(ksp_density.keys())
y_ksp = list(ksp_density.values())
x_model = list(density_for_high.keys())
y_model = list(density_for_high.values())

plt.plot(x_model, y_model, color='green', label='Model')
plt.plot(x_ksp, y_ksp, color='orange', label='KSP Data')
plt.xlabel('Высота, км')
plt.ylabel('Плотность воздуха, кг/м^3')
plt.title('График зависимости плотности воздуха от высоты')
plt.legend()
plt.grid(True)
plt.show()