import adafruit_servokit
index = 0
angleTranslation = [[90,1],[130,1],[130,1],[40,1],[90,1],[0,1]]
angles = [0, 0, -40, 50, 0, 40]
park = [0,0,20,-10,0,70]
limits = [[0,180],[0,180],[0,180],[0,180],[0,180],[0,70]]
limits2 = [[-90,90],[-130,50],[-130,150],[-40,120],[-90,90],[0,70]]
kit = adafruit_servokit.ServoKit(channels = 16)
def switchServo(direction):
    global index
    if index + direction > 5:
        index = 0
    elif index + direction <0:
        index = 5
    else:
        index += direction
    
def parkArm():
        parkAngles = park
        for i in range(6):
            target = translateAngle(i,parkAngles[i])
            try:
                kit.servo[i].angle = target
            except ValueError:
                print(f"out of range: {target} Servo: {i}")
def setAngles():
        parkAngles = angles
        for i in range(6):
            target = translateAngle(i,parkAngles[i])
            try:
                kit.servo[i].angle = target
            except ValueError:
                print(f"out of range: {target} Servo: {i}")

def translateAngle(index,angle):
    servoAngle= angleTranslation[index][0]+ angle*angleTranslation[index][1]
    return servoAngle
def translateAngleReverse(index,angle):
    servoAngle= angleTranslation[index][0]+ angle*-angleTranslation[index][1]
    return servoAngle

def translateAngleArray():
        servoAngleArray=[]
        for i in range(len(angles)):
            servoAngleArray.append(translateAngleReverse(i,angles[i]))
        return servoAngleArray

parkArm()
setAngles()
while True:
    print("======================================================")
    print(angles)
    print(f"Servo {index}: {angles[index]}")
    
    i = input()
    if(i == "a"):
        switchServo(-1)
    if(i == "d"):
        switchServo(+1)
    if(i =="q"):
        parkArm()
    try:
        x = translateAngle(index,int(i))
        if x >= limits[index][0] and x <= limits[index][1]:
            angles[index] = int(i)
            kit.servo[index].angle = x
        else:
            print(f"out of range: {x} Servo: {i}")
    except ValueError:
        print("valuerror")
        continue

