import keyboard  # using module keyboard
import time
switchDelay = 0.3
anglechangeDelay = 0.1
index = 0

angles = [90,90,90,90,90,90]
limits = [[0,180],[0,180],[0,180],[0,180],[0,180],[0,180]]

class _Getch:       
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
    inkey = _Getch()
    while(1):
            k=inkey()
            if k!='':break
    print(f"you pressed {ord(k)}")
    

def changeAngle(angle):
    if angles[index] + angle >= limits[index][0] and angles[index] +angle <= limits[index][1]:
        angles[index] += angle
        print(f"Servo {index}: {angles[index]}")
    time.sleep(anglechangeDelay)
    
    
def switchServo(direction):
    global index
    if index + direction > 5:
        index = 0
    elif index + direction <0:
        index = 5
    else:
        index += direction
    print(f"Servo {index}: {angles[index]}")
    time.sleep(switchDelay)

while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        modifier = 1
        if keyboard.is_pressed('left shift'):
            modifier = 10
        if keyboard.is_pressed('up arrow'):  # if key 'q' is pressed 
            changeAngle(+1 * modifier)
        if keyboard.is_pressed('down arrow'):  # if key 'q' is pressed 
            changeAngle(-1 * modifier)
        if keyboard.is_pressed('left arrow'):  # if key 'q' is pressed 
            switchServo(-1)
        if keyboard.is_pressed('right arrow'):  # if key 'q' is pressed 
            switchServo(+1)
        if keyboard.is_pressed('return'):
            print(angles)
            time.sleep(switchDelay)
            
    except:
        continue  # if u