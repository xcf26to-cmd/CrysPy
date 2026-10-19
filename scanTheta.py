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
t0 = time.time()

rate1 = []
delta_angle = 0.2* u.deg

step0 = Pi.Angle2Step(0, 0-5*delta_angle)
#Pi.MoveTheta(step0)
print(f"Initially moved to -{5*delta_angle} deg")
p0, r0 = ScanLineSearcher(Pi)
breakpoint()
rate1.append(r0)

for i in range(1,11):
    Pi.MoveTheta(Pi.Angle2Step(0, delta_angle))
    p, r = ScanLineSearcher(Pi)
    rate1.append(r)
    print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = +{(i)*delta_angle}")
    if (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] < 0):
        break
        
print(rate1)
'''
max_angle_rate = np.max(rate1)
index = np.where(rate1 == max_angle_rate)[0][0]
print(index)
step_final = Pi.Angle2Step(0, -(len(rate1)-index -2) * delta_angle)
Pi.MoveTheta(step_final)
print(f"After fast scan, moved to {-(len(rate1)-index -2) * delta_angle}, the index after the max")
print(f"Numero di step: {step_final}")
'''

rate2 = []
delta_angle_2 = 0.05* u.deg

p2, r2 = ScanLineSearcher(Pi)
rate2.append(r2)

i=0
for i in range(0,8):
    Pi.MoveTheta(Pi.Angle2Step(0, -delta_angle_2))
    p, r = ScanLineSearcher(Pi)
    rate2.append(r)
    print(f"fast scan... i ={i} Max rate = {r} Hz, Position = {p} mm, Angle = -{(i+1)*delta_angle_2}")
    if r > max_angle_rate*0.95:
        exit()

#se supera il massimo deve fermarsi e fare lo scan piccolo
#se il rate aumenta agli estremi dello scan, continua lo scan
