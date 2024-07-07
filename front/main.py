from machine import UART, Pin, Timer, ADC
import time

frame_time = 2
sleep_time = 11
compte = 0

control_led = Pin(25, Pin.OUT)

#Déclaration des entrées analogiques vers numérique pour les capteurs de force
C1 = ADC(28)
#C2 = ADC(27)

calib_pad = 395


S1 = Pin(19, Pin.IN, Pin.PULL_DOWN)
S2 = Pin(18, Pin.IN, Pin.PULL_DOWN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             )

color_mode = 0

uart_in = UART(0, 115200, rx =13, tx =12)
uart_in.init(115200, bits=8, parity=None, stop=1)

uart_out = UART(1,115200, rx =9, tx = 8)
uart_out.init(115200, bits=8, parity=None, stop=1)

def _on_ADC_timeout() :
    
    global uart_in
    global uart_out
    global calib_pad
    
    global S1
    global S2
    global color_mode
    global control_led
    
    if S1.value() :
        color_mode = 1
    elif S2.value() :
        color_mode = 2
    else :
        color_mode = 0
    #print(color_mode)
    
    data =uart_in.read()
    if data is not None :
        control_led.on()
        #print(data[2:4])
    #formatage des mesures pour l'envoi par UART et ajout de la mesure manquante (Pad1)
        vpad = max(0,(min(20000,C1.read_u16())-calib_pad)/(20000-calib_pad))*65535
    #print(vpad)
        message = int.to_bytes(int(vpad),2,1)
    #Lectures des mesures du coprocesseur (Pad 2,3,4,5)
    
        #print(data)
        message += data
        #Ajout des mesures manquantes (Hue et modes de couleur (aléatoire ou controlée))
        message+= int.to_bytes(color_mode,1,0)
    
        #Envoi du message
        #print(message)
        uart_out.write(message)
    else :
        control_led.off()


while 1 :
    
    if compte == 0 :
        _on_ADC_timeout()
    else :
        control_led.off()
    
    compte = (compte+1)%frame_time
    time.sleep_ms(sleep_time)

#Décalration et Déclanchement du Timer (actualisation des mesures toutes les 16 ms)