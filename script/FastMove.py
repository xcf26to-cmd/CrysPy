import os, sys
#repo root (parent of script/) so PiMove, Point, ... are importable from anywhere
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from PiMove   import PiMikro

Pi = PiMikro()
while True:
    print('Do you need PyMicro?')
    if input()=='no':
        break
    print('Which axe should I move?')
    axe = input()
    print('Position?')
    pos = input()
    print(f'Moving {axe} in {pos}')
    Pi.MoveThat(str(axe), float(pos), velocity = 3)
