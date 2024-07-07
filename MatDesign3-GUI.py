import math
import tkinter as tk
from tkinter import ttk, messagebox

# Define the main calculation function
def calculate_and_check(P1, P2, P3, q_g, FS, C, L_cr, L_cl, F_y, E):
    P = P1 + P2 + P3  # Total lift load in tonnes

    # Initial effective length of the mat plate
    L_eff = (P * FS * 9.81) / (q_g * L_cl)  # Initial calculation in meters
    L_eff = round(L_eff, 0)  # Round up to the nearest whole number

    # Function to perform calculations and checks
    def perform_checks(L_eff, t_eff):
        q = P * 9.81 / (L_eff * L_cl)  # Actual bearing pressure in kilopascals
        L_c = (L_eff - C) / 2  # Cantilever portion length in meters
        M = 1/2 * (L_c**2) * q * L_cl  # Max moment in kilonewton-meters (kNm)
        V = q * L_c * L_cl  # Total shear force in kilonewtons (kN)
        F_v = 1.5 * V / (L_cl * t_eff)  # Maximum shear stress in megapascals (MPa)
        F_va = 0.6 * F_y  # Allowable shear stress in megapascals (MPa)
        W = 0.00785 * t_eff * L_cl * L_eff  # Weight of the mat in tonnes
        q_pw = (P + W) * 9.81 / (L_eff * L_cl)  # Bearing pressure including mat weight
        delta = (q * L_cl * L_c**4 / ((8 * E * 1000 * L_eff * (t_eff / 1000)**3) / 12)) * 1000  # Mat deflection in millimeters
        delta_a = 0.75 / 100 * (L_eff * 1000)  # Allowable deflection in millimeters

        bearing_pressure_check = q_pw > (q_g / FS)
        shear_stress_check = F_va < F_v
        deflection_check = delta > delta_a
        mat_length_check = L_eff > L_cr / 2 + (C + L_c)

        return bearing_pressure_check, shear_stress_check, deflection_check, mat_length_check, L_eff, t_eff, q_pw, F_v, delta

    bearing_pressure_check = True
    t_eff = math.sqrt(6 * ((1/2 * (((L_eff - C)/2)**2) * (P * 9.81 / (L_eff * L_cl)) * L_cl) / (L_cl * 0.6 * F_y * 1000))) * 1000
    t_eff = round(t_eff / 5) * 5  # Round to the nearest 5mm

    while bearing_pressure_check:
        bearing_pressure_check, shear_stress_check, deflection_check, mat_length_check, L_eff, t_eff, q_pw, F_v, delta = perform_checks(L_eff, t_eff)
        if mat_length_check:
            messagebox.showwarning("Warning", "The mat length is greater than the distance between two crawler crane chains (inner edge). Please revise the mat material")
            return None, None, None, None, None
        if bearing_pressure_check:
            L_eff += 0.25

    while shear_stress_check or deflection_check:
        t_eff += 5
        bearing_pressure_check, shear_stress_check, deflection_check, mat_length_check, L_eff, t_eff, q_pw, F_v, delta = perform_checks(L_eff, t_eff)

    if mat_length_check:
        messagebox.showwarning("Warning", "The mat length is greater than the distance between two crawler crane chains (inner edge). Please revise the mat material")
        return None, None, None, None, None

    return L_eff, t_eff, q_pw, F_v, delta

# Define the GUI application
class MatDesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crawler Crane Mat Design")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Input fields
        self.inputs = {}
        input_labels = [
            "Total lift load (P1) [tonnes]:", "Crane weight (P2) [tonnes]:", "Counterweight (P3) [tonnes]:",
            "Soil ultimate bearing capacity (q_g) [kPa]:", "Factor of safety (FS):", "Width of the crawler crane chain (C) [m]:",
            "Distance between two crawler crane chains (L_cr) [m]:", "Length of the crawler crane chain (L_cl) [m]:",
            "Yield strength of the mat plate (F_y) [MPa]:", "Modulus of elasticity (E) [MPa]:"
        ]
        default_values = [140, 20, 200, 145, 2, 1.5, 12, 12.570, 250, 200000]

        for i, (label_text, default_value) in enumerate(zip(input_labels, default_values)):
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(self.root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, default_value)
            self.inputs[label_text] = entry

        # Calculate button
        self.calculate_button = ttk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=len(input_labels), column=0, columnspan=2, pady=10)

    def calculate(self):
        try:
            # Gather inputs
            P1 = float(self.inputs["Total lift load (P1) [tonnes]:"].get())
            P2 = float(self.inputs["Crane weight (P2) [tonnes]:"].get())
            P3 = float(self.inputs["Counterweight (P3) [tonnes]:"].get())
            q_g = float(self.inputs["Soil ultimate bearing capacity (q_g) [kPa]:"].get())
            FS = float(self.inputs["Factor of safety (FS):"].get())
            C = float(self.inputs["Width of the crawler crane chain (C) [m]:"].get())
            L_cr = float(self.inputs["Distance between two crawler crane chains (L_cr) [m]:"].get())
            L_cl = float(self.inputs["Length of the crawler crane chain (L_cl) [m]:"].get())
            F_y = float(self.inputs["Yield strength of the mat plate (F_y) [MPa]:"].get())
            E = float(self.inputs["Modulus of elasticity (E) [MPa]:"].get())

            # Perform calculation
            L_eff, t_eff, q_pw, F_v, delta = calculate_and_check(P1, P2, P3, q_g, FS, C, L_cr, L_cl, F_y, E)
            
            if L_eff is not None:
                # Show results in a new window
                result_window = tk.Toplevel(self.root)
                result_window.title("Calculation Results")

                results = {
                    "Effective Length (L_eff) [m]": L_eff,
                    "Minimum Thickness (t_eff) [mm]": t_eff,
                    "Allowable Bearing Stress [kPa]": q_pw,
                    "Allowable Shear Stress [MPa]": F_v,
                    "Deflection [mm]": delta
                }

                for i, (label_text, result) in enumerate(results.items()):
                    label = ttk.Label(result_window, text=f"{label_text}: {result:.2f}")
                    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            else:
                messagebox.showwarning("Warning", "Calculation did not converge. Please check your inputs and try again.")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MatDesignApp(root)
    root.mainloop()
