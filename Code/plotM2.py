import pandas as pd
import matplotlib.pyplot as plt


# ---- Load CSV files ----
# df_min  = pd.read_csv("code/output/integration_output_340km.csv")
# df_mean = pd.read_csv("code/output/integration_output_380km.csv")
# df_max  = pd.read_csv("code/output/integration_output_420km.csv")
df_original  = pd.read_csv("Code/output/integration_output_380km.csv")
df_min  = pd.read_csv("Code/output/M2_min_380km_final.csv")
df_mean = pd.read_csv("Code/output/M2_avg_380km_final.csv")
df_max  = pd.read_csv("Code/output/M2_max_380km_final.csv")

# Convert radius to km
df_original['Radius_km']  = df_original['Radius']  / 1000.0
df_min['Radius_km']  = df_min['Radius']  / 1000.0
df_mean['Radius_km'] = df_mean['Radius'] / 1000.0
df_max['Radius_km']  = df_max['Radius']  / 1000.0

# Extract radius and profiles
r_original, rho_original = df_original['Radius_km'], df_original['Density']
r_min,  rho_min  = df_min['Radius_km'],  df_min['rho_new']
r_mean, rho_mean = df_mean['Radius_km'], df_mean['rho_new']
r_max,  rho_max  = df_max['Radius_km'],  df_max['rho_new']

# ---- Create plots ----


# Mass profile
plt.plot(rho_mean, r_mean, label="T_avg", linewidth=2)
plt.plot(rho_min,  r_min,  linestyle=":", label="T_min")
plt.plot(rho_max,  r_max,  linestyle=":", label="T_max")
plt.plot(rho_original, r_original, linestyle="--", label="Original 380 km")
plt.xlabel("Density (kg/m³)")
plt.ylabel("Radius (km)")
plt.grid(True)
plt.legend()


plt.tight_layout()
# plt.savefig("Code/output/MinMax_Mass_Gravity_Pressure_Profiles.png", dpi=400)
plt.show()