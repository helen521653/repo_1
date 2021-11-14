import spidev
import time
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import waveFunctions as w

#length = 1430mm
w.initSpiAdc()
w.waitForOpen()
start = time.time()
samples = []
start = time.time()
while (time.time() - start < 30):
    samples.append(w.getAdc())
finish = time.time()
w.saveMeasures(samples, len(samples), 1,start, finish)
    
plt.plot(samples)
plt.show()
w.deinitSpiAdc()
