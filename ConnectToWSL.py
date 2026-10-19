import subprocess
import glob
import os
from datetime import datetime as dt

def callps1(path='./', livetime='15', name='', function = ''):
    powerShellPath = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
    #absolute path: works whatever the current working directory is
    powerShellCmd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script.ps1')
    print('Ready')
    #call script with argument '/mnt/c/Users/aaa/'
    p = subprocess.Popen([powerShellPath, '-ExecutionPolicy', 'Unrestricted', '-File', powerShellCmd, path, livetime, name, function]
                         , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    #WSL output is UTF-16 in some cases: decode leniently
    output = output.decode(errors='replace').replace('\x00', '')
    error = error.decode(errors='replace').replace('\x00', '')
    if p.returncode != 0 or error.strip():
        print(f"[callps1] returncode={p.returncode}\n[stdout]\n{output}\n[stderr]\n{error}")
        raise RuntimeError("SDD acquisition through WSL failed")
    return 1

def CheckForFile(path):
    print("checking...")
    path = 'C:/Users/XCF/'+path
    while True:
        check = glob.glob(path+f'/file_{dt.now().year}_{dt.now().month}_{dt.now().day}_{dt.now().hour}_{dt.now().minute}.npz')
        if len(check)>0:
            print('Done')
            return 1
