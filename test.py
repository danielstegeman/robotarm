#import gpio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time
import enum
from Robotarm import Order
import socket
import pickle
kit = ServoKit(channels=16)

parkAngles = [0,80,10,-90,0,80]
target = [0,100,-110,0,45,0]
#robot = Order(parkAngles,20)
#kit.servo[2].angle = 100
#print(kit.servo[2].angle)
# #robot.animateToPosition(target,20)
# robot.setPosition(target)
#robot.animateToPosition(parkAngles,20)


orderDict = {
        "OrderId":0, #unique id given to each order for modification
        "TargetPosition":[], #array of 6 angles as a target
        "AnimationDuration": 0,
        "InsertionMode":"First/Interrupt", #Adds the order to the front of the queue to be executed after
        "Command":"Park/Hold"
        }
      
def SendOrder():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost',5000))
    data = pickle.dumps(orderDict)
    
    sock.sendall(data)
    sock.sendall(data)
SendOrder()