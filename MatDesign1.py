import math

# Input variables
P1 = 140  # Total lift load in tonnes
P2 = 20   # Crane weight in tonnes
P3 = 200  # Counterweight in tonnes
q_g = 145  # Soil ultimate bearing capacity in kilopascals
FS = 2  # Factor of safety
C = 1.5  # Width of the crawler crane chain in meters
L_cr = 12  # Distance between two crawler crane chain (inner edge) in meters
L_cl = 12.570  # Length of the crawler crane chain in meters
F_y = 250  # Yield strength of the mat plate in megapascals for A36 steel plates 
E = 200000  # Modulus of elasticity in megapascals

# Calculate total lift load in kilonewtons
P = P1 + P2 + P3  # P is in tonnes

# Calculate the length of the crawler crane mat plate in meters
L = (P * FS * 9.81) / (q_g * L_cl)  # L is in meters
L_eff = round(L * 4) / 4  # Round up to the nearest quarter of the whole number, L_eff is in meters

# Calculating the actual bearing pressure 
q = P * 9.81 / (L_eff * L_cl)  # q is in kilopascals

# Determine the mat's cantilever portion length
L_c = (L_eff - C)/2  # L_c is in meters

# Calculate the max moment underneath the cantilever mat
M = 1/2 * (L_c**2) * q * L_cl  # M is in kilonewton-meters (kNm)

# Calculate the minimum thickness of the mat
t = math.sqrt(6 * M / (L_cl * 0.6 * F_y * 1000)) * 1000  # t is in millimeters (mm)

# Round up to the nearest 5mm
t_eff = round(t / 5) * 5  # t_eff is in millimeters (mm)

# Maximum shear stress in the mat
V = q * L_c * L_cl  # V is in kilonewtons (kN), V is the total shear force
F_v = 1.5 * V / (L_cl * t_eff)  # F_v is in megapascals (MPa)
F_va = 0.6 * F_y  # Allowable shear stress, F_y is in megapascals (MPa)

# Check if the allowable shear stress is greater than the actual shear stress
if F_va < F_v:
    print("The mat thickness is not enough to resist the shear stress")

# Calculate the weight of the mat
W = 0.00785 * t_eff * L_cl * L_eff  # W is in tonnes   

# Calculate the bearing pressure including mat weight 
q_pw = (P + W) * 9.81 / (L_eff * L_cl)  # q_pw is in kilopascals (kPa)

# Check if the bearing pressure is less than the allowable bearing pressure
if q_pw > (q_g / FS):
    print("The bearing pressure is greater than the allowable bearing pressure")

# Calculate mat deflection
delta = (q * L_cl * L_c**4 / ((8 * E * 1000 * L_eff * (t_eff / 1000)**3) / 12)) * 1000  # delta is in millimeters (mm)

# Allowable deflection is 0.75% of the effective length of the mat
delta_a = 0.75 / 100 * (L_eff * 1000)  # delta_a is in millimeters (mm)

# Check if the deflection is greater than the allowable deflection
if delta > delta_a:
    print("The deflection is greater than the allowable deflection")

# Check if the mat length for eahc chain exceeded the limit of L_cr
if L_eff > L_cr/2+(C+L_c):
    print("The mat length is greater than the distance between two crawler crane chain (inner edge). please revise the mat material")






#print the total lift load in tonnes
print("Total lift load (P):", P)

#print the length of the crawler crane mat plate in meters
print("Mat length (L):", L)

#print the actual bearing pressure
print("Actual bearing pressure (q):", q)

#print the effective length of the mat plate
print("Effective length of mat plate (L_eff):", L_eff)

#print the cantilever portion length of the mat plate
print("Cantilever portion length (L_c):", L_c)

#print the maximum moment underneath the cantilever mat
print("Maximum moment (M):", M)

#print the effective thickness of the mat
print("Effective thickness of the mat (t_eff):", t_eff)

#print the maximum shear stress in the mat
print("Maximum shear stress (F_v):", F_v)

#print the allowable shear stress
print("Allowable shear stress (F_va):", F_va)

#print the bearing pressure including mat weight
print("Bearing pressure including mat weight (q_pw):", q_pw)
print("Allowable bearing pressure including mat weight (q_g/FS):",q_g/FS)

#print allowable mat deflection
print("Allowable deflection (delta_a):", delta_a)

#print the mat deflection
print("Mat deflection (delta):", delta)

