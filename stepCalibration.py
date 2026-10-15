import argparse as ar
from astropy import units as u
import numpy as np
from PiMove   import PiMikro
from SDDscan import StandardScan, MeasureEnergy, ScanLineSearcher
from utils import fmt_err, LogTheta
import time
import matplotlib.pyplot as plt


#Connect to SDD
Pi = PiMikro()

rate1 = []
rate2 = []
step1 = np.linspace(0,-60000,25)
step2 = np.linspace(-57500,0,24)

t0 = time.time()
Pi.MoveTheta(30000)
print("Initially moved by +30000 steps")
step = -2500

p0, r0 = ScanLineSearcher(Pi)
rate1.append(r0)

i=0
for i in range(0,24):
    Pi.MoveTheta(step)
    p, r = ScanLineSearcher(Pi)
    rate1.append(r)
    print(f"fast scan... i ={i} Max rate = {r} Hz, Position = {p} mm, Steps = {(i+1)*step}")
    print(f"Cumulative time: {time.time()-t0} s")

print(rate1)
print("changing direction")
j=0
for j in range(0,24):
    Pi.MoveTheta(-step)
    p, r = ScanLineSearcher(Pi)
    rate2.append(r)
    print(f"fast scan... j ={j} Max rate = {r} Hz, Position = {p} mm, Steps = {-(j+1)*step}")
    print(f"Cumulative time: {time.time()-t0} s")

t1 = time.time()
print(f"Scan ended in {np.round(t1 - t0, 1)} s")

print(rate2)
plt.figure()
plt.plot(step1, rate1, linestyle = "-", marker = "o", label = "da 0 a -60000")
plt.plot(step2, rate2, linestyle = "-", marker = "o", label = "da -57500 a 0")
plt.xlabel("steps")
plt.ylabel("rate [Hz]")
plt.grid(True)
plt.legend()
plt.show()
