import spidev
import time
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt

import waveFunctions as w
w.initSpiAdc()

samples = []
start = time.time()
while (time.time() - start < 10):
    samples.append(w.getAdc())
finish = time.time()
w.saveMeasures(samples, len(samples), 1,start, finish)
    
