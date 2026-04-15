import numpy
import matplotlib.pyplot as plt
import math
from scipy.signal import argrelextrema

F1H = [1]
FC_H = [1]
FH = [1]
SGP_H = 0
fS_H = 0
max_x_FH = []
max_y_FH = []
min_x_FH = []
min_y_FH = []

F1E = [1]
FC_E = [1]
FE = [1]
SGP_E = 0
fS_E = 0
max_x_FE = []
max_y_FE = []
min_x_FE = []
min_y_FE = []
steps = [0]

lambd = 0.029
a = 0.14
b = 0.14

for teta in numpy.arange(0.01, numpy.pi / 2, 0.00001):

    mn1E = abs((1 + numpy.cos(teta))/ 2)
    mn2E = abs(math.sin((numpy.pi * b * math.sin(teta)) / lambd) / (numpy.pi * b * math.sin(teta) / lambd))
    mn3E = mn1E * mn2E

    F1E.append(mn1E)
    FC_E.append(mn2E)
    FE.append(mn3E)

    mn1H = abs((1 + numpy.cos(teta)) / 2)
    mn2H = abs(numpy.cos((numpy.pi * a * numpy.sin(teta)) / lambd)) / abs(1 - ((2 * a * numpy.sin(teta)) / lambd) ** 2)
    mn3H = mn1H * mn2H

    F1H.append(mn1H)
    FC_H.append(mn2H)
    FH.append(mn3H)

    steps.append(math.degrees(teta))

    if 0.707 < mn3H < 0.708:
        SGP_H = 2 * math.degrees(teta)
        fS_H = mn3H

    if 0.707 < mn3E < 0.708:
        SGP_E = 2 * math.degrees(teta)
        fS_E = mn3E

for i in range(1, len(FH) - 1):

    if FH[i] > FH[i - 1] and FH[i] > FH[i + 1]:
        max_x_FH.append(steps[i])
        max_y_FH.append(FH[i])

    if FH[i] < FH[i - 1] and FH[i] < FH[i + 1]:
        min_x_FH.append(steps[i])
        min_y_FH.append(0)

    if FE[i] > FE[i - 1] and FE[i] > FE[i + 1]:
        max_x_FE.append(steps[i])
        max_y_FE.append(FE[i])

    if FE[i] < FE[i - 1] and FE[i] < FE[i + 1]:
        min_x_FE.append(steps[i])
        min_y_FE.append(0)

print("\nШирина головної пелюстки:")
print("H =", round(SGP_H, 2), "°")
print("E =", round(SGP_E, 2), "°")
print("\nПерші бокові пелюстки:")
print("H =", round(max_y_FH[0], 3))
print("E =", round(max_y_FE[0], 3))

print("\nВаріант = 5")
print(f"Довжина хвилі = {lambd} м")
print(f"Розмір розкриву рупора а*b = {a} x {b} м")
print("\nТабл. 1 - Значення нульових кутів")
print("----------------")
print("| № |  θ  |FE(θ)|")
print("----------------")

for i in range(len(min_x_FE)):
    if i < 3:
        print(f"| {i+1} |{min_x_FE[i]:5.2f}|  0  |")
print("----------------")
print("Табл. 2 - Значення максимальних кутів")
print("----------------")
print("| № |  θ  |FE(θ)|")
print("----------------")

for i in range(len(max_x_FE)):
    if i < 3:
        print(f"| {i+1} |{max_x_FE[i]:5.2f}|{max_y_FE[i]:5.2f}|")
print("----------------")

print(f"\nШирина головної пелюстки в площині E = {SGP_E:.2f}°")
print(f"\nШирина головної пелюстки в площині H = {SGP_H:.2f}°")


fig, ax = plt.subplots(figsize=(20/2.54, 12/2.54))
ax.plot(steps, F1H, linewidth=0.7, label="$ F_{1h}(θ) $")
ax.plot(steps, FC_H, label="$ F_{2h}(θ) $")
ax.plot(steps, FH, label="$ F_{H}(θ) $")
ax.plot(SGP_H/2, fS_H, 'ro', markersize=4, label="Рівень половинної потужності в площині H")
plt.annotate(f'({fS_H:.3f}, {SGP_H/2:.2f}\u00b0)',
             xy=(SGP_H / 2, fS_H),
             xytext=((SGP_H/2)+3, fS_H+0.05),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=6)
ax.plot([0, SGP_H/2], [fS_H, fS_H], 'r--', linewidth=0.5)
ax.plot([SGP_H/2, SGP_H/2], [0, fS_H], 'r--', linewidth=0.5)
ax.plot(max_x_FH, max_y_FH, "o", markersize=4, color="black", label="$ \\theta_{max} $ FH")
ax.plot(min_x_FH, min_y_FH, "o", markersize=4, color="blue", label="$ \\theta_{min} $ FH")
ax.set_xlabel('θ' + '\u00b0', fontsize=10)
ax.set_ylabel('|Fh(θ' + '\u00b0' + ')|, |F1h(θ' + '\u00b0' + ')|', fontsize=10)
plt.xticks(numpy.arange(0, 100, 2), fontsize=7)
plt.yticks(numpy.arange(0, 1.2, 0.1), fontsize=7)
plt.ylim(-0.01, 1.01)
plt.xlim(0, 90.5)
plt.legend(loc="upper right", fontsize=7)
plt.grid(which='both', linestyle='--', linewidth=0.2, color='gray')
plt.show()
fig.savefig("ДС у площині H.jpg", dpi=600)
plt.show()

fig, ax = plt.subplots(figsize=(20/2.54, 12/2.54))
ax.plot(steps, F1E, linewidth=0.7, label="$ F_{1e}(θ) $")
ax.plot(steps, FC_E, label="$ F_{2e}(θ) $")
ax.plot(steps, FE, label="$ F_{E}(θ) $")
ax.plot(SGP_E/2, fS_E, 'go', markersize=4, label="Рівень половинної потужності в площині E")
plt.annotate(f'({fS_E:.3f}, {SGP_E/2:.2f}\u00b0)',
             xy=(SGP_E / 2, fS_E),
             xytext=((SGP_E/2)-13, fS_E+0.05),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=6)
ax.plot([0, SGP_E/2], [fS_E, fS_E], 'r--', linewidth=0.5)
ax.plot([SGP_E/2, SGP_E/2], [0, fS_E], 'r--', linewidth=0.5)
ax.plot(max_x_FE, max_y_FE, "o", markersize=4, color="black", label="$ \\theta_{max} $ FE")
ax.plot(min_x_FE, min_y_FE, "o", markersize=4, color="blue", label="$ \\theta_{min} $ FE")
ax.set_xlabel('θ' + '\u00b0', fontsize=10)
ax.set_ylabel('|Fe(θ' + '\u00b0' + ')|, |F1e(θ' + '\u00b0' + ')|', fontsize=10)
plt.xticks(numpy.arange(0, 100, 2), fontsize=7)
plt.yticks(numpy.arange(0, 1.2, 0.1), fontsize=7)
plt.ylim(-0.01, 1.01)
plt.xlim(0, 90.5)
plt.legend(loc="upper right", fontsize=7)
plt.grid(which='both', linestyle='--', linewidth=0.2, color='gray')

plt.show()
fig.savefig("ДС у площині E.jpg", dpi=600)
plt.show()