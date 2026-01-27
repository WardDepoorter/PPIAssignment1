import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# ---- Load CSV files ----
# df_min  = pd.read_csv("code/output/integration_output_340km.csv")
# df_mean = pd.read_csv("code/output/integration_output_380km.csv")
# df_max  = pd.read_csv("code/output/integration_output_420km.csv")
df_min  = pd.read_csv("code/output/M2_min_380km_final.csv")
df_mean = pd.read_csv("code/output/M2_avg_380km_final.csv")
df_max  = pd.read_csv("code/output/M2_max_380km_final.csv")

# Convert radius to km
df_min['Radius_km']  = df_min['Radius']  / 1000.0
df_mean['Radius_km'] = df_mean['Radius'] / 1000.0
df_max['Radius_km']  = df_max['Radius']  / 1000.0

# Extract radius and profiles
r_min,  M_min,  g_min,  P_min  = df_min['Radius_km'],  df_min['Mass'],  -df_min['Gravity'],  df_min['Pressure']
r_mean, M_mean, g_mean, P_mean = df_mean['Radius_km'], df_mean['Mass'], -df_mean['Gravity'], df_mean['Pressure']
r_max,  M_max,  g_max,  P_max  = df_max['Radius_km'],  df_max['Mass'],  -df_max['Gravity'], df_max['Pressure']

# ---- Create plots ----
fig, axs = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

# Mass profile
axs[0].plot(M_mean, r_mean, label="T_avg", linewidth=2)
axs[0].plot(M_min,  r_min,  linestyle=":", label="T_min")
axs[0].plot(M_max,  r_max,  linestyle=":", label="T_max")
axs[0].set_xlabel("Mass (kg)")
axs[0].set_ylabel("Radius (km)")
axs[0].grid(True)
axs[0].legend()

# Gravity profile
axs[1].plot(g_mean, r_mean, linewidth=2)
axs[1].plot(g_min,  r_min,  linestyle=":")
axs[1].plot(g_max,  r_max,  linestyle=":")
axs[1].set_xlabel("Gravity (m/s²)")
axs[1].grid(True)

# Pressure profile
axs[2].plot(P_mean, r_mean, linewidth=2)
axs[2].plot(P_min,  r_min,  linestyle=":")
axs[2].plot(P_max,  r_max,  linestyle=":")
axs[2].set_xlabel("Pressure (GPa)")
axs[2].grid(True)

plt.tight_layout()
# plt.savefig("Code/output/MinMax_Mass_Gravity_Pressure_Profiles.png", dpi=400)
plt.show()
#calculate mass error from observed value
M_observed = 7.34948e22 # kg
print('final mass T_min:', M_min.iloc[-1])
print('final mass T_avg:', M_mean.iloc[-1])

print('final mass T_max:', M_max.iloc[-1])
m_error_min  = abs(M_min.iloc[-1]  - M_observed)/M_observed * 100
m_error_mean = abs(M_mean.iloc[-1] - M_observed)/M_observed * 100
m_error_max  = abs(M_max.iloc[-1]  - M_observed)/M_observed * 100


print(f"Mass error T_min:  {m_error_min:.6f} %")
print(f"Mass error T_avg: {m_error_mean:.6f} %")
print(f"Mass error T_max:  {m_error_max:.6f} %")

#calculate MOI from density profile:
def calculate_moi(radii_km, densities_kg_m3):
    radii_m = radii_km * 1000.0
    dr = 100 #nodes spacing in meters
    moi_integral = (2/5) * (densities_kg_m3 * (radii_m ** 4) * dr).sum()
    total_mass = (densities_kg_m3 * (4/3) * np.pi * (radii_m ** 3) * dr).sum()
    moi = moi_integral / total_mass
    return moi
moi_min  = calculate_moi(r_min,  df_min['rho_new'])
moi_mean = calculate_moi(r_mean, df_mean['rho_new'])
moi_max  = calculate_moi(r_max,  df_max['rho_new'])
print(f"MOI T_min:  {moi_min:.6f}")
print(f"MOI T_avg: {moi_mean:.6f}")
print(f"MOI T_max:  {moi_max:.6f}")