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
#First scan
rate1 = []
delta_angle = 0.2* u.deg
dir = 0

ScanLineSearcher(Pi)
step0 = Pi.Angle2Step(0, 0-5*delta_angle)
Pi.MoveTheta(step0)
print(f"Initially moved to -{5*delta_angle} deg")
p0, r0 = ScanLineSearcher(Pi)
rate1.append(r0)

for i in range(1,11):
    Pi.MoveTheta(Pi.Angle2Step(0, delta_angle))
    p, r = ScanLineSearcher(Pi)
    rate1.append(r)
    print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = +{(i)*delta_angle}")
    if (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] < 0) and (i-2 >= 0) and (rate1[i-1] - rate1[i-2] > 0):
        #caso 1: il rate diminuisce dopo aver trovato il massimo (dopo essere aumentato)
        print("Max rate found")
        dir = -1
        break
    if (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] < 0):
        #caso 4: il rate diminuisce, ma non è mai aumentato
        i0 = i
        i+=1
        print(f"Max rate is before the scan, changing direction at angle = +{(i0)*delta_angle}")
        Pi.MoveTheta(Pi.Angle2Step(0, -delta_angle))
        p, r = ScanLineSearcher(Pi)
        rate1.append(r)
        print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = -{(i-i0)*delta_angle}")
        while (rate1[i] - rate1[i-1] > 0) and (rate1[i] > 20):
            i+=1
            Pi.MoveTheta(Pi.Angle2Step(0, -delta_angle))
            p, r = ScanLineSearcher(Pi)
            rate1.append(r)
            print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = -{(i-i0)*delta_angle}")
        dir = +1
        break

     
if (rate1[-1] - rate1[-2] > 0) and (rate1[-1] > 20):
    #caso 2: il rate aumenta alla fine dello scan, deve continuare
    print("Max rate is after the scan, continuing")
    i+=1
    Pi.MoveTheta(Pi.Angle2Step(0, delta_angle))
    p, r = ScanLineSearcher(Pi)
    rate1.append(r)
    print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = +{(i)*delta_angle}")
    while (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] > 0):
        i+=1
        Pi.MoveTheta(Pi.Angle2Step(0, delta_angle))
        p, r = ScanLineSearcher(Pi)
        rate1.append(r)
        print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = +{(i)*delta_angle}")
    dir = -1

if (np.max(rate1) < 20):
    #caso 3: la riga non è nel range in cui si è fatto lo scan in angolo, e neanche agli estremi, serve cercare oltre
    print("Max rate not found, continuing the scan")
    for i in range(11,16):
        Pi.MoveTheta(Pi.Angle2Step(0, delta_angle))
        p, r = ScanLineSearcher(Pi)
        rate1.append(r)
        print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = +{(i)*delta_angle}")
        if (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] < 0) and (rate1[i-1] - rate1[i-2] > 0):
            print("Max rate found")
            dir = -1
            break
        if (rate1[-1] - rate1[-2] > 0) and (rate1[-1] > 20):
            #caso 3.2: il rate aumenta alla fine dello scan, deve continuare
            print("Max rate is after the scan, continuing")
            i+=1
            Pi.MoveTheta(Pi.Angle2Step(0, delta_angle))
            p, r = ScanLineSearcher(Pi)
            rate1.append(r)
            print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = +{(i)*delta_angle}")
            while (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] > 0):
                i+=1
                Pi.MoveTheta(Pi.Angle2Step(0, delta_angle))
                p, r = ScanLineSearcher(Pi)
                rate1.append(r)
                print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = +{(i)*delta_angle}")
            dir = -1
            break
    if (np.max(rate1) < 20):
        #caso 3.3: la riga non è nel range in cui si è fatto lo scan in angolo, serve tornare indietro per vedere se è prima
        print(f"Max rate not found, changing direction and moving by -{14*delta_angle}")
        Pi.MoveTheta(Pi.Angle2Step(0, -14*delta_angle))
        i1=1
        for i in range(16,22):
            Pi.MoveTheta(Pi.Angle2Step(0, -delta_angle))
            p, r = ScanLineSearcher(Pi)
            rate1.append(r)
            print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = -{(i-i1)*delta_angle}")
            if (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] < 0) and (rate1[i-1] - rate1[i-2] > 0):
                print("Max rate found")
                dir = +1
                break
            if (rate1[-1] - rate1[-2] > 0) and (rate1[-1] > 20):
                #caso 3.3.2: il rate aumenta alla fine dello scan, deve continuare
                print("Max rate is after the scan, continuing")
                i+=1
                Pi.MoveTheta(Pi.Angle2Step(0, -delta_angle))
                p, r = ScanLineSearcher(Pi)
                rate1.append(r)
                print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = -{(i-i1)*delta_angle}")
                while (rate1[i-1] > 20) and (rate1[i] - rate1[i-1] > 0):
                    i+=1
                    Pi.MoveTheta(Pi.Angle2Step(0, -delta_angle))
                    p, r = ScanLineSearcher(Pi)
                    rate1.append(r)
                    print(f"fast scan... i ={i-1} Max rate = {r} Hz, Position = {p} mm, Angle = -{(i-i1)*delta_angle}")
                dir = +1
                break 
        
t1 = time.time()
print(f"First scan ended in {t1-t0} s")
max_angle_rate = np.max(rate1)
print(f"Max rate of the first scan = {max_angle_rate} Hz")

#Second scan
rate2 = []
delta_angle_2 = 0.05* u.deg

p2, r2 = ScanLineSearcher(Pi)
rate2.append(r2)
#dir = +1 -> si sposta di + delta_angle_2
#dir = -1 -> si sposta di - delta_angle_2

for i in range(0,8):
    Pi.MoveTheta(Pi.Angle2Step(0, dir*delta_angle_2))
    p, r = ScanLineSearcher(Pi)
    rate2.append(r)
    print(f"fast scan... i ={i} Max rate = {r} Hz, Position = {p} mm, Angle = -{(i+1)*delta_angle_2}")
    if r > max_angle_rate*0.95:
        break

#se supera il massimo deve fermarsi e fare lo scan piccolo
#se il rate aumenta agli estremi dello scan, continua lo scan
t2 = time.time()
print(f"Second scan ended in {t2-t1} s, total time: {t2-t0} s")