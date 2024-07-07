import math

# Input variables
P1 = 140  # Total lift load in tonnes
P2 = 20   # Crane weight in tonnes
P3 = 200  # Counterweight in tonnes
q_g = 145  # Soil ultimate bearing capacity in kilopascals
FS = 2  # Factor of safety
C = 1.5  # Width of the crawler crane chain in meters
L_cr = 12  # Distance between two crawler crane chain (outer edge) in meters
L_cl = 12.570  # Length of the crawler crane chain in meters
F_y = 250  # Yield strength of the mat plate in megapascals for A36 steel plates 
E = 200000  # Modulus of elasticity in megapascals

# Calculate total lift load in tonnes
P = P1 + P2 + P3  # P is in tonnes

# Initialize effective length of the mat plate
L_eff = (P * FS * 9.81) / (q_g * L_cl)  # Initial calculation in meters
L_eff = round(L_eff, 0)  # Round up to the nearest whole number, L_eff is in meters

# Function to perform the calculations and checks
def calculate_and_check(L_eff, t_eff):
    # Calculating the actual bearing pressure 
    q = P * 9.81 / (L_eff * L_cl)  # q is in kilopascals

    # Determine the mat's cantilever portion length
    L_c = (L_eff - C)/2  # L_c is in meters

    # Calculate the max moment underneath the cantilever mat
    M = 1/2 * (L_c**2) * q * L_cl  # M is in kilonewton-meters (kNm)

    # Maximum shear stress in the mat
    V = q * L_c * L_cl  # V is in kilonewtons (kN), V is the total shear force
    F_v = 1.5 * V / (L_cl * t_eff)  # F_v is in megapascals (MPa)
    F_va = 0.6 * F_y  # Allowable shear stress, F_y is in megapascals (MPa)

    # Calculate the weight of the mat
    W = 0.00785 * t_eff * L_cl * L_eff  # W is in tonnes   

    # Calculate the bearing pressure including mat weight 
    q_pw = (P + W) * 9.81 / (L_eff * L_cl)  # q_pw is in kilopascals (kPa)

    # Calculate mat deflection
    delta = (q * L_cl * L_c**4 / ((8 * E * 1000 * L_eff * (t_eff / 1000)**3) / 12)) * 1000  # delta is in millimeters (mm)

    # Allowable deflection is 0.75% of the effective length of the mat
    delta_a = 0.75 / 100 * (L_eff * 1000)  # delta_a is in millimeters (mm)

    # Check if the bearing pressure is less than the allowable bearing pressure
    bearing_pressure_check = q_pw > (q_g / FS)
    
    # Check if the allowable shear stress is greater than the actual shear stress
    shear_stress_check = F_va < F_v

    # Check if the deflection is greater than the allowable deflection
    deflection_check = delta > delta_a
    
    # Check if the mat length for each chain exceeded the limit of L_cr
    mat_length_check = L_eff > L_cr / 2 + (C + L_c)
    
    return bearing_pressure_check, shear_stress_check, deflection_check, mat_length_check, L_eff, t_eff

# Iteratively increase the effective length until the bearing pressure condition is satisfied
bearing_pressure_check = True
t_eff = math.sqrt(6 * ((1/2 * (((L_eff - C)/2)**2) * (P * 9.81 / (L_eff * L_cl)) * L_cl) / (L_cl * 0.6 * F_y * 1000))) * 1000
t_eff = round(t_eff / 5) * 5  # Round to the nearest 5mm

while bearing_pressure_check:
    bearing_pressure_check, shear_stress_check, deflection_check, mat_length_check, L_eff, t_eff = calculate_and_check(L_eff, t_eff)
    if mat_length_check:
        print("The mat length is greater than the distance between two crawler crane chain (inner edge). Please revise the mat material")
        break
    if bearing_pressure_check:
        L_eff += 0.25

# Iteratively increase the thickness until the shear stress and deflection conditions are satisfied
while shear_stress_check or deflection_check:
    t_eff += 5
    bearing_pressure_check, shear_stress_check, deflection_check, mat_length_check, L_eff, t_eff = calculate_and_check(L_eff, t_eff)

# Output the effective length and thickness of the mat plate
if not mat_length_check:
    print(f"The effective length of the mat plate is: {L_eff} meters")
    print(f"The minimum thickness of the mat plate is: {t_eff} millimeters")



