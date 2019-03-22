#Test labjack python code
import time
from psychopy.hardware.labjacks import U3

lj = u3.U3()
print(lj.configIO(FIOAnalog = 252))
starttime=time.time()
while True:
    if (time.time() - starttime) % 1 == 0:
        print "pulse"
