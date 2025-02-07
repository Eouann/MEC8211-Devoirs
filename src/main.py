#############################
#Importation de bibliothèques
#############################
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


###########################
# Définition des constantes
###########################
Ntot = 5          # nombre de point pour la méthodes des différences finies
Deff = 10e-10     # en m^2/s
Ce = 20           # en mol/m^3
D = 1             # en m
R = D/2           # en m
S = 2e-8          # en mol/m^3/s


######################################
# Définition de la fonction analytique
######################################
r = sp.symbols('r')
C = sp.Function('C')
C_r = 0.25*S/Deff*R**2*(r**2/R**2 - 1) + Ce

# Transformation de la fonction analytique sympy en fonction traçable par matplotlib
C_analytique = sp.lambdify(r, C_r, modules=['numpy'])
x_values = np.linspace(0, R, 500)
y_values = C_analytique(x_values)


#####################################################
# Calcul en différences finies pour Ntot points CAS 1
#####################################################
delta_r=R/(Ntot-1)
r_i=np.zeros(Ntot)          # Vecteur des N points r_i également espacées
for i in range(len(r_i)):
    r_i[i] = delta_r*i

# Calcul des coefficients devant les Ci+1, Ci et Ci-1

# CAS 1
a1=np.zeros(Ntot)       # Coefficient devant Ci+1
b1=np.zeros(Ntot)       # Coefficient devant Ci
c1=np.zeros(Ntot)       # Coefficient devant Ci-1
for i in range(1,len(r_i)):
    a1[i]=1/delta_r**2+1/(r_i[i]*delta_r)
    b1[i]=-(2/delta_r**2+1/(r_i[i]*delta_r))
    c1[i]=1/delta_r**2

# CAS 2
a2=np.zeros(Ntot)       # Coefficient devant Ci+1
b2=np.zeros(Ntot)       # Coefficient devant Ci
c2=np.zeros(Ntot)       # Coefficient devant Ci-1
for i in range(1,len(r_i)):
    a2[i]=1/delta_r**2+1/(r_i[i]*2*delta_r)
    b2[i]=-2/delta_r**2
    c2[i]=1/delta_r**2-1/(r_i[i]*2*delta_r)

def Concentrations(a,b,c):
    # Fonction de calcul des N concentrations en différences finies
    C_i = np.zeros(Ntot)
    matA = np.zeros((Ntot,Ntot))
    vectB = np.zeros(Ntot)

    # Condition de Neumann à i = 0
    matA[0,0] = 1
    matA[0,1] = -1
    vectB[0] = 0

    # Condition de Dirichlet à i = N
    matA[-1,-1] = 1
    vectB[-1] = Ce

    # Algorithmes differences finies
    for i in range(1,len(C_i)-1):
        matA[i,i-1] = c[i]
        matA[i,i] = b[i]
        matA[i,i+1] = a[i]

        vectB[i] = S/Deff

    C_i = np.linalg.solve(matA,vectB)
    return C_i

Concentrations_CAS1=Concentrations(a1,b1,c1)
Concentrations_CAS2=Concentrations(a2,b2,c2)

# Tracé des fonctions analytiques et différences finies
plt.figure()
plt.plot(x_values, y_values)
plt.plot(r_i, Concentrations_CAS1, 'o', color='red')
plt.plot(r_i, Concentrations_CAS2, 'o', color='green')
plt.show()