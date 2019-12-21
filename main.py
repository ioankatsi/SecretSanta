import serial
from playsound import playsound
import multiprocessing, threading
import time
import RPi.GPIO as GPIO

# init Rapsberry Pi Pins for leds and switch
led_green = 17
led_red = 18
switch = 26
init_led_time = 1
first_step = False
second_step = True

# Open Serial Port Communication
ser = serial.Serial('/dev/ttyACM0', 9600)

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(led_red, GPIO.LOW)
GPIO.output(led_green, GPIO.HIGH)

def thread_function(sound):
    '''
    function that plays a sound effect
    '''
    playsound('sounds/' + sound + '.mp3')

ai_talk = ["defused", "hello_dimitris", "joke_start", "i_dont_ask", "joke", "haha", "congrats_defuse","next_riddle", "riddle_2", "ai_hint", "hint", "mitsos_player"]

#bomb init
while True:
    if GPIO.input(switch) == GPIO.LOW:
        print(GPIO.input(switch))
        time.sleep(0.2)
    elif GPIO.input(switch) == GPIO.HIGH:
        #print('Bomb Planted')
        GPIO.output(led_green, GPIO.LOW)
        break

# Blink Red faster while time passes
for i in range(10):
    GPIO.output(led_red, GPIO.HIGH)
    time.sleep(init_led_time)
    GPIO.output(led_red, GPIO.LOW)
    time.sleep(init_led_time)
    init_led_time -= 0.1
    if init_led_time <= 0.1:
        for _ in range(10):
            GPIO.output(led_red, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(led_red, GPIO.LOW)
            time.sleep(0.1)

# Bomb defuse begins
while True:
    p = multiprocessing.Process(target=thread_function, args=['planted'])
    p.start()
    time.sleep(2)
    GPIO.output(led_red, GPIO.HIGH)
    time.sleep(2)
    pwd = []
    while first_step == False:
        if(ser.in_waiting > 0): # Check for incoming data from arduino
            line = ser.readline()
            pwd.append(line.decode("utf-8").replace("\r\n",""))
            print(line.decode("utf-8"))
            if len(pwd) < 4 :
                continue
            elif len(pwd) == 4:
                print(pwd)
                # DUMMY way to check for right PIN
                if pwd[0] == '5' and pwd[1] == '4' and pwd[2] == '3' and pwd[3] == '5':
                    pwd = []
                    second_riddle = True
                    pass
                else:
                    pwd = []
                    thread_function('wrong_answer')
                    continue

            GPIO.output(led_red, GPIO.LOW)
            GPIO.output(led_green, GPIO.HIGH)
            p.terminate()
            time.sleep(0.5)

            for sound in ai_talk:
                thread_function(sound)
                time.sleep(0.5)
            time.sleep(1)
            GPIO.output(led_green, GPIO.LOW)
            time.sleep(1)
            GPIO.output(led_red, GPIO.HIGH)
            time.sleep(1)
            p = multiprocessing.Process(target=thread_function, args=['millionaire'])
            p.start()
            pwd=[]
            while second_riddle == True:
                if(ser.in_waiting> 0):
                    line = ser.readline()
                    pwd.append(line.decode("utf-8").replace("\r\n",""))
                    print(line.decode("utf-8"))
                    if len(pwd) < 4 :
                        continue
                    elif len(pwd) == 4 :
                        print(len(pwd))
                        print(pwd[0], pwd[1], pwd[2], pwd[3])
                        if pwd[0] == '1' and pwd[1] == '3' and  pwd[2] == '1' and pwd[3] == '2':
                            p.terminate()
                            time.sleep(0.5)
                            thread_function('you-win-sound-effect-5')
                            p.terminate()
                            for i in range(10):
                                GPIO.output(led_red, GPIO.HIGH)
                                GPIO.output(led_green, GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(led_red, GPIO.LOW)
                                GPIO.output(led_green, GPIO.LOW)
                                time.sleep(0.1)
                            exit()
                        else:
                            print(len(pwd))
                            print(type(pwd[0]))
                            print(pwd[0], pwd[1], pwd[2], pwd[3])
                            pwd = []
                            thread_function('wrong_answer')
                            continue
