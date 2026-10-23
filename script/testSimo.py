import os, sys
#repo root (parent of script/) so PiMove, Point, ... are importable from anywhere
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PiMove import PiMikro

test=PiMikro()
test.MovePhi(10000)
