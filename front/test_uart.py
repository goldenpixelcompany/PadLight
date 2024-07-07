from machine import UART
from machine import Pin
import time

uart_in = UART(0, 9600, rx =13, tx =12)
uart_in.init(9600, bits=8, parity=None, stop=2)

control_led = Pin(25, Pin.OUT)

#uart_out = UART(1,9600)
#uart_out.init(9600, bits=8, parity=None, stop=1)
#print('starting uart...')
control_led.on()
time.sleep(.5)
control_led.off()
time.sleep(.5)
control_led.on()
time.sleep(.5)
control_led.off()
time.sleep(.5)
control_led.on()
time.sleep(.5)
control_led.off()
time.sleep(.5)

for i in range(30):
    
    uart_in_data = uart_in.read()
    print(uart_in_data)
    if uart_in_data is not None :
        control_led.on()
        print(int.from_bytes(uart_in_data,0))
    else :
        control_led.off()
    
    
    time.sleep(1)