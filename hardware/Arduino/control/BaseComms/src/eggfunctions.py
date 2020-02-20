import sys
import serial

# def whichCommand(key):
#     switcher = {
#         'w':1,
#         's':2,
#         'a':3,
#         'd':4,
#         'p':5
#     }
#     numb = switcher.get(key)
#     return "echo -ne '{0}/n' > /dev/ttyACM0".format(numb)

def whichCommandNumber(key):
    switcher = {
        'w':1,
        's':2,
        'a':3,
        'd':4,
        'p':5
    }
    return switcher.get(key)+'/n'


def getKey():
    key = ''
    while not(key=='w' or key=='a' or key=='s' or key=='d' or key=='p'):
        key = input().lower()
        if not(key=='w' or key=='a' or key=='s' or key=='d' or key=='p'):
            print("Try Again")
    return key


def keyboardControl():
    key = getKey()
    return whichCommandNumber(key)
        

def main():
    ser = serial.Serial('/dev/ttyACM0')
    print(ser.name)
    while(1):
        command = whichCommandNumber()
        print(command)
        ser.write(command)
    ser.close()

if __name__ == "__main__":
    main()