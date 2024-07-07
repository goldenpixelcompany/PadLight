import machine
from machine import PWM
import math
import time

rgb1 = [PWM(2, freq=1000,duty_u16=0),
        PWM(3, freq=1000,duty_u16=0),
        PWM(4, freq=1000,duty_u16=0)]

rgb2 = [PWM(5, freq=1000,duty_u16=0),
        PWM(6, freq=1000,duty_u16=0),
        PWM(7, freq=1000,duty_u16=0)]

rgb3 = [PWM(8, freq=1000,duty_u16=0),
        PWM(9, freq=1000,duty_u16=0),
        PWM(10, freq=1000,duty_u16=0)]

rgb4 = [PWM(11, freq=1000,duty_u16=0),
        PWM(14, freq=1000,duty_u16=0),
        PWM(15, freq=1000,duty_u16=0)]

rgb5 = [PWM(18, freq=1000,duty_u16=0),
        PWM(19, freq=1000,duty_u16=0),
        PWM(20, freq=1000,duty_u16=0)]

all_pix = [rgb1,rgb2 ,rgb3,rgb4,rgb5]
#all_pix = [rgb4]

def set_duty_cycle_percent(val,out) :
    if val > 1. :
        val = 1
    elif val < 0. :
        val = 0.
    out.duty_u16(int(val*65535))
    #print(val)
 
compte = 0
while 1 :
    for pix in all_pix :
        print(compte)
        for out in pix:
            print(out)

            for i in range(1000) :
                if i < 500 :
                    set_duty_cycle_percent(float(i)/500.,out)
                else :
                    set_duty_cycle_percent(1.-float(i-500)/500.,out)
            
                time.sleep_ms(4)
            
            for pwm in pix :
                pwm.duty_u16(0)
        compte += 1
