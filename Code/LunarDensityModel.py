# from https://github.com/rorycockshaw/VPREMOON


import numpy as np 
import matplotlib.pyplot as plt

strdata = open("Code/VPREMOON.txt").read()
strdata = strdata.replace("\n", "")
strdata = strdata.replace("\t", ",")

strdata = strdata.split(",")

strradii = []
strvp = []
strvs = []
strrho = []
i = 0
while i < len(strdata) / 10 - 1: 
    strradii.append(strdata[10 * i])
    strvp.append(strdata[10 * i + 1])
    strvs.append(strdata[10 * i + 2])
    strrho.append(strdata[10 * i + 3])
    i+=1

radii = np.array([])
vp = np.array([])
vs = np.array([])
rho = np.array([])

for j in strradii: 
    radii = np.append(radii,float(j))
for j in strvp: 
    vp = np.append(vp,float(j))
for j in strvs: 
    vs = np.append(vs,float(j))
for j in strrho: 
    rho = np.append(rho,float(j))


k = 0
while k < len(radii) - 1: 
    xvalues = [radii[k],radii[k+1]]
    yvalues = [rho[k],rho[k+1]]
    plt.plot(yvalues,xvalues)
    k+=1

plt.title("Lunar density against radius")
plt.ylabel("Radius/km")
plt.xlabel("Density/g $cm^-3$")
    
plt.show() 

plt.clf()