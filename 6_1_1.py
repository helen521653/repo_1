import  RPi.GPIO as GPIO 
import time
import matplotlib.pyplot as plt

def decimal2binary(decimal):
    return[int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac,signal)
    return signal


dac = [26,19,13,6,5,11,9,10]
leds =[21,20,16,12,7,8,25,24]

bits = len(dac)
comp = 4
levels = 2** bits
maxVoltage = 3.3
troykaModule = 17
value_znach = [0]
voltage_step = maxVoltage / levels
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT , initial = GPIO.LOW)
GPIO.setup(leds,GPIO.OUT , initial = GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)
period = 0.005
frequency = 1 / period

#Демонстрация на leds
def show_on_leds(signal):
    signal = decimal2binary(value)
    GPIO.output(leds, signal)

#Определение U на comporator

def adc():
    for i in range(8):
        GPIO.output(dac,0)
        time.sleep(0.0007)
        value = 0
        for i in range(8):
            value = value + 2**(7 - i)
            signal = bin2dac(value)
            time.sleep(period)
            compValue = GPIO.input(comp)
            if compValue == 0:
                value = value - 2**(7 - i)
            voltage = value / levels * maxVoltage
        return value
    print (" Digital value: {:^3} -> {}, Analog value: {:.2f}".format(value, signal, voltage))

    


try:
    GPIO.output(troykaModule, 1)
    print("Началась зарядка ")
    start_t= time.time()
    print('Конденсатор заряжается')
    while True:
        value = adc()
        value_znach.append(value)
        print(value)
        show_on_leds(value)
        if value == 249:
            GPIO.output(troykaModule, 0)
            break
    print("Конденсатор разряжается")    
    #Считывания напряжения при разрядке
    while True:
        value = adc()
        value_znach.append(value)
        print(value)
        show_on_leds(value)
        if value == 5:
            finish_t = time.time()
            break 
    print('Конденсатор разрядился')
    all_time_experiment = finish_t - start_t

    #Параметры эксперимента
    print("Длительность эксперимента=", all_time_experiment, "c Период измерений=", period, "c Частота дискретизации=", frequency, "Гц Шаг напряжения=", voltage_step, "В")
    #График
    plt.plot(value_znach)
    plt.show()



    #Работа с файлом
    value_array_str = [str(item) for item in value_znach]
    with open("data.txt", "w") as f:
        f.write("\n".join(value_array_str))
    parametrs = [all_time_experiment, all_time_experiment, frequency, frequency]
    parametrs_str = [str(item) for item in parametrs]
    with open("settings.txt", "w") as f1:
        f1.write("\n".join(parametrs_str))

finally:
    
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.cleanup(leds)

 
