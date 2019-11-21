from playsound import playsound
import multiprocessing, threading
import time


# print to screen
# Hello dimitris for security reasons
# i have to know that your are the one

def thread_function(sound):
    playsound('sounds/' + sound + '.mp3')

ai_talk = ["hello_dimitris", "joke_start", "i_dont_ask", "joke", "haha"]
while True:
    p = multiprocessing.Process(target=thread_function, args=['planted'])
    p.start()
    time.sleep(4)
    while True:
        if (input("Enter your code : ") != str(1234)):
            print("try again")
        else:
            print('ok')
            p.terminate()

            time.sleep(2)
            for sound in ai_talk:
                thread_function(sound)
                time.sleep(1)


            exit(0)
