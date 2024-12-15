import json
import matplotlib.pyplot as plt
from math import exp, log

# Constants
H_0 = 55 * 1000  # Height of start of fall in meters
R = 8.31  # Universal gas constant
P_0 = 506625  # Average atmospheric pressure at sea level in Pa

h_1 = 5000  # m
p_1 = 316277  # Pa
h_2 = 10000  # m
p_2 = 182072  # Pa

H = (h_2 - h_1) / log(p_1 / p_2)


pressure_for_high = {}
for high in range(56):
     pressure = P_0 * exp(-high * 1000 / H)
     pressure_for_high[high] = pressure / 101325

with open("flight_atmosphere_pressure (1).json", encoding="UTF-8") as file_in:
    ksp_data = json.load(file_in)

ksp_pressure = {}

for altitude, pressure in ksp_data.items():
    ksp_pressure[float(altitude) / 1000] = pressure / 101325


x_ksp = list(ksp_pressure.keys())
y_ksp = list(ksp_pressure.values())
x_model = list(pressure_for_high.keys())
y_model = list(pressure_for_high.values())


plt.plot(x_model, y_model, color='green', label='Model')
plt.plot(x_ksp, y_ksp, color='orange', label='KSP Data')
plt.xlabel('Высота, км')
plt.ylabel('Давление, атм')
plt.title('График зависимости давления от высоты')
plt.legend()
plt.grid(True)
plt.show()
