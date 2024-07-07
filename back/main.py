from machine import UART, Pin, Timer, ADC, PWM
import time
from random import randint, randrange, random, choice, uniform

uart_in = UART(0, 115200, rx =17, tx =16)
uart_in.init(115200, bits=8, parity=None, stop=1)


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

rgb5 = [PWM(22, freq=1000,duty_u16=0),
        PWM(28, freq=1000,duty_u16=0),
        PWM(27, freq=1000,duty_u16=0)]

all_pix = [rgb1,rgb2 ,rgb3,rgb4,rgb5]

frame_time = 2
sleep_time = 11
compte = 0

control_led = Pin(25, Pin.OUT)

def random_color() :
    rcolor = [0,0,0]
    for i in range(3) :
        rcolor[i] = random()
    
    bright = randint(0,3)
    for i in range(bright) :
        rcolor[randint(0,2)] = uniform(.3,1.)
    
    #print(' COLOR  : ',rcolor)
    return rcolor


Uni_color1 = random_color()
Uni_color2 = random_color()
R_color = [random_color(),random_color(),random_color(),random_color(),random_color()]
R_can_change = [True,True,True,True,True]

color_mode = 0

t_color_mode = 0
t_pix_lum = [0,0,0,0,0]


def send_colors() :
    global all_pix
    global color_mode
    global t_pix_lum
    global Uni_color1
    global Uni_color2
    global R_color
    global R_can_change
    
    #print('color_mode ',color_mode)
    
    if color_mode == 0 :
        for i in range(len(all_pix)) :
            for j in range(len(all_pix[i])):
                all_pix[i][j].duty_u16(int(t_pix_lum[i]*Uni_color1[j]))
                #print(i,' ',j,'sended c : ',int(t_pix_lum[i]*Uni_color1[j]))
    
    elif color_mode == 1 :
        for i in range(len(all_pix)) :
            for j in range(len(all_pix[i])):
                all_pix[i][j].duty_u16(int(t_pix_lum[i]*Uni_color2[j]))
                #print(i,' ',j,'sended c : ',int(t_pix_lum[i]*Uni_color2[j]))
    elif color_mode == 2 :
        for i in range(len(all_pix)) :
            if t_pix_lum[i] >= 60000 and R_can_change[i] :
                #print('color change')
                R_can_change[i] = True
                R_color[i] = random_color()
            elif t_pix_lum[i] < 500 :
                R_color[i] = random_color()
                R_can_change[i] = False
                
            for j in range(len(R_color[i])) :
                all_pix[i][j].duty_u16(int(t_pix_lum[i]*R_color[i][j]))
                #print(i,' ',j,'sended c : ',int(t_pix_lum[i]*R_color[j]))
    


def _on_ADC_timeout() :
    global uart_in
    global all_pix
    global t_color_mode
    global color_mode
    global t_pix_lum
    
    data =uart_in.read()
    if data is not None :
        control_led.on()
        
        for i in range(len(t_pix_lum)):
            t_pix_lum[i] = int.from_bytes(data[(i*2):((i+1)*2)],0)
            
        #print(t_pix_lum)
        t_color_mode = int.from_bytes(data[10:],0)
        #print(t_color_mode)
        
        if t_color_mode is not color_mode :
            if t_color_mode == 0 :
                #print('mode 0')
                Uni_color1 = random_color()
            elif t_color_mode == 1 :
                #print('mode 1')
                Uni_color2 = random_color()
            
        color_mode = t_color_mode
        
        send_colors()
    
    

while 1 :
    
    if compte == 0 :
        _on_ADC_timeout()
    else :
        control_led.off()
    
    compte = (compte+1)%frame_time
    time.sleep_ms(sleep_time)