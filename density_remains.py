import json
import matplotlib.pyplot as plt
from math import exp, log

# КОНСТАНТЫ
H_0 = 55 * 10 ** 3
R = 8.31
M = 0.044
g = 16.7  
p_0 = 6.517

h_1 = 5000
p_1 = 4.633
h_2 = 10000
p_2 = 3.036 

H = (h_2 - h_1) / log(p_1 / p_2)

density_remains = {}
new_density = {}

with open("flight_atmosphere_density (1).json", encoding="UTF-8") as file_in:
    ksp_data = json.load(file_in)

ksp_density = {}

for altitude, density in ksp_data.items():
    ksp_density[float(altitude) / 1000] = density

for high in ksp_density.keys():
    density1 = p_0 * exp(-int(high) * 1000 / H)
    new_density[high] = density1
    density_remains[high] = ksp_density[high] - density1


with open("density_for_remains.json", "w", encoding="UTF-8") as file_out:
    json.dump([new_density], file_out, ensure_ascii=False, indent=2)


x = [key for key in density_remains.keys()]
y = [value for value in density_remains.values()]
plt.plot(x, y, color='blue')
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('Высота, км')
plt.ylabel('Остатки, кг/м^3')
plt.title('Погрешность при вычислении плотности воздуха')
plt.show()
