import pandas as pd
import matplotlib.pyplot as plt

# ---- Load CSV files ----
df_min  = pd.read_csv("code/output/integration_output_340km.csv")
df_mean = pd.read_csv("code/output/integration_output_380km.csv")
df_max  = pd.read_csv("code/output/integration_output_420km.csv")

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
axs[0].plot(M_mean, r_mean, label="380 km", linewidth=2)
axs[0].plot(M_min,  r_min,  linestyle=":", label="340 km")
axs[0].plot(M_max,  r_max,  linestyle=":", label="420 km")
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