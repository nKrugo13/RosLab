import numpy as np
import matplotlib.pyplot as plt 
import math
import cmath


EpsilonParticle = 2.2135 * (10 ** -11)
ConductivityParticle = 3.9 * (10 ** -3)

EpsilonMedium = 6.95 * (10 ** -10)
ConductivityMedium = 1.81 * (10 ** -2)

Dielectric_FreeSpace = 8.854 * (10 ** -12)


DeltaEpsilon1 = EpsilonParticle - EpsilonMedium
DeltaSigma1 = ConductivityMedium - ConductivityParticle
DeltaEpsilon2 = EpsilonParticle + 2 * EpsilonMedium
DeltaSigma2 = ConductivityParticle - 2 * ConductivityMedium




def NEW_Derived_EQ(DeltaEpsilon1, DeltaSigma1, DeltaEpsilon2, DeltaSigma2, f):
    A = DeltaEpsilon1
    B = DeltaSigma1 * ((2*np.pi)/f)
    C = DeltaEpsilon2
    D = DeltaSigma2 * ((2*np.pi)/f)

    Top = A*C + B*D + 1j*(B*C-A*D)
    Bottom = C**2 + D**2

    result = Top/ Bottom
    
    return result


f_values = np.linspace(1, 1000000000, 100000)  
only_conductance_result = (ConductivityParticle-ConductivityMedium)/(ConductivityParticle+2*ConductivityMedium)
print(only_conductance_result)
# Calculate results for each f value
results = []

for f in f_values:
    result = NEW_Derived_EQ(DeltaEpsilon1, DeltaSigma1, DeltaEpsilon2, DeltaSigma2, f)
    if result > 1:
        print('Over')
    elif result < -0.5:
        print("Under")
    results.append(np.real(result))  # Take the real part for plotting
f_value_LOG = [math.log(f) for f in f_values]

#print('Results: ')
#print(results)
# Plot
plt.plot((f_values), results)
plt.xlabel('Frequency')
#plt.xscale('log')
plt.ylabel('Real CM')
plt.title('Plot of Real CM vs Frequency')
plt.grid(True)
plt.show()