from AmptekControl import SDD
from matplotlib import pyplot as plt
import numpy as np
import argparse as ar

formatter = ar.ArgumentDefaultsHelpFormatter
parser = ar.ArgumentParser(formatter_class=formatter)
parser.add_argument('-path', type=str, help='npz file path', default='./', required=False)
parser.add_argument('-time', type=str, help='livetime', default='120', required=False)
parser.add_argument('-name', type=str, help='name', default='', required=False)
parser.add_argument('-function', type=str, help='function(r, e, s)', default='', required=True)
args = parser.parse_args()

Amp = SDD()



def rate(args):
    print("Acquiring Rate")
    with open('/mnt/c/Users/XCF/' + args.path + "rate.txt", "w") as f:
        f.write(str(Amp.GetRate()))
        f.close()

def energy(args):
    print("Acquiring Energy")
    _, _, par, cov = Amp.Acquire(livetime=float(args.time))
    with open('/mnt/c/Users/XCF/' + args.path + "energy.txt", "w") as f:
        for element in par:
            f.write(str(element)+"\n")
        f.write(str(cov[0][0])+"\n")
        f.write(str(cov[1][1])+"\n")
        f.write(str(cov[2][2])+"\n")
        f.close()

def standardSDD(args):
    print("Acquiring Spectrum")
    data, utilData = Amp.SaveAndAcquire(livetime=time, path=path, name=args.name)

if __name__== "__main__":
    if args.path == './':
        path = '/mnt/c/Users/XCF/'
    else:
        path = '/mnt/c/Users/XCF/' + args.path
    print(path)
    if args.function == "r":
        rate(args)
    elif args.function == "e":
        energy(args)
    else:
        standardSDD(args)
