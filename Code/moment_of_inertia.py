import pandas as pd
import numpy as np


csv_avg = 'Code/output/M2_min_380km_final.csv'

# Read the CSV file
df_avg = pd.read_csv(csv_avg)

# Extract radius and density
radius = df_avg['Radius'].values  # in meters
rho = df_avg['rho_new'].values  # density in kg/m^3
# Calculate the moment of inertia for each shell
# For a spherical shell: dI = (8π/3) * ρ(r) * r^4 * dr

# Calculate dr (step size)
dr = np.diff(radius)

# For each shell, use the radius at the center of the shell
# and calculate the contribution to moment of inertia
I_total = 0.0

for i in range(len(radius) - 1):
    r_mid = (radius[i] + radius[i+1]) / 2  # midpoint radius
    rho_mid = (rho[i] + rho[i+1]) / 2  # average density in shell
    
    # Moment of inertia contribution from this shell
    dI = (8 * np.pi / 3) * rho_mid * r_mid**4 * dr[i]
    I_total += dI

print(f"Total Moment of Inertia: {I_total:.6e} kg·m²")

# Calculate the normalized moment of inertia factor (I/MR²)
# First get the total mass and radius
M_total = df_avg['Mass'].iloc[-1]  # Total mass from last row
R_moon = radius[-1]  # Moon's radius

I_MR2 = I_total / (M_total * R_moon**2)
print(f"\nMoon's total mass: {M_total:.6e} kg")
print(f"Moon's radius: {R_moon:.2f} m")
print(f"Normalized moment of inertia (I/MR²): {I_MR2:.6f}")
print(f"\nFor reference:")
print(f"  Uniform sphere: I/MR² = 0.4")
print(f"  Observed Moon: I/MR² ≈ 0.3932")
# Observed Moon's moment of inertia factor is approximately 0.3932
moi_observed = 0.3932
error = abs(I_MR2 - moi_observed) / moi_observed * 100
print(f"Percentage error from observed value: {error:.6f} %")
