import os, sys
#repo root (parent of script/) so PiMove, Point, ... are importable from anywhere
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import PiMove as pm

dchain = pm.PiMikro()
dchain.HotSpot(3.45,-1.3)
#chain.HotSpot(0, 0)
dchain.Cobra(amplitude=4)
