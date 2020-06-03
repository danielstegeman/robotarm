#import gpio

# from adafruit_servokit import ServoKit
import time
import enum
# from Robotarm import Order
import socket
import pickle
# kit = ServoKit(channels=16)

parkAngles = [0,80,10,-90,0,80]
target = [0,100,-110,0,45,0]
#robot = Order(parkAngles,20)
#kit.servo[2].angle = 100
#print(kit.servo[2].angle)
# #robot.animateToPosition(target,20)
# robot.setPosition(target)
#robot.animateToPosition(parkAngles,20)
idcounter = 0

orderDict = {
        "OrderId":0, #unique id given to each order for modification
        "TargetPosition":[], #array of 6 angles as a target
        "AnimationDuration": 0,
        "InsertionMode":"First/Interrupt", #Adds the order to the front of the queue to be executed after
        "Command":"Park/Hold"
        }
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendOrder(animationDuration,targetPosition = None, command = None, insertionMode = None):
    orderDict = {
        "OrderId":idcounter,
        "AnimationDuration": animationDuration}
    if targetPosition != None:
        orderDict["TargetPosition"] = targetPosition
    if command != None:
        orderDict["Command"] = command
    if insertionMode != None:
        orderDict["InsertionMode"] = insertionMode
    data = pickle.dumps(orderDict)
    data = data + b"|"
    sock.sendall(data) #use socket instance here
    print(data)
    


sock.connect(('localhost',45283))   

sendOrder(1,command= "Raise")
sendOrder(1,command="Lower")
sendOrder(1,command="Raise")
sendOrder(1,command="Lower")
sendOrder(3,command="Park")