#import gpio

# from adafruit_servokit import ServoKit
import time
import random
import enum
# from Robotarm import Order
import socket
import pickle
# kit = ServoKit(channels=16)
from OrderManager import OrderManager
parkAngles = [0, 80, 10, -90, 0, 80]
target = [0, 100, -110, 0, 45, 0]
#robot = Order(parkAngles,20)
#kit.servo[2].angle = 100
# print(kit.servo[2].angle)
# #robot.animateToPosition(target,20)
# robot.setPosition(target)
# robot.animateToPosition(parkAngles,20)
idcounter = 0
manager = OrderManager()

orderDict = {
        "OrderId": 0,  # unique id given to each order for modification
        "TargetPosition": [],  # array of 6 angles as a target
        "AnimationDuration": 0,
        # Adds the order to the front of the queue to be executed after
        "InsertionMode": "First/Interrupt",
        "Command": "Park/Hold"
}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendOrder(animationDuration, targetPosition=None, command=None, insertionMode=None):
    # sock.connect(('localhost', 59321))
    orderDict = {
        "OrderId": idcounter,
        "AnimationDuration": animationDuration}
    if targetPosition != None:
        orderDict["TargetPosition"] = targetPosition
    if command != None:
        orderDict["Command"] = command
    if insertionMode != None:
        orderDict["InsertionMode"] = insertionMode
    # data = pickle.dumps(orderDict)
    # data = data + b"|"
    # sock.send(data)  # use socket instance here
    # sock.close()
    manager.recievedOrders.put(orderDict)
    # print(data)




duration = 1


def rpsdemo():
    x = random.randrange(3)
    sendOrder(duration, command="Raise")
    sendOrder(duration, command="Lower")
    sendOrder(duration, command="Raise")
    sendOrder(duration, command="Lower")
    sendOrder(duration, command="Raise")

    startTime = time.perf_counter()

    if(x == 0):
        sendOrder(duration, command="Rock")
        print("rock")
    elif x == 1:
        sendOrder(duration, command="Paper")
        print("paper")
    elif x == 2:
        sendOrder(duration, command="Cissor")
        print("cissors")
    # while(time.perf_counter()- startTime <30):
    #     continue
    # sendOrder(10,command="Park")
    return


def betterrps():
    
    while True:
        i = input()
        if(i == "f"):
            sendOrder(duration, command="Raise")
        if(i == 's'):
            
            sendOrder(duration, command="Lower")
            sendOrder(duration, command="Raise")
            sendOrder(duration, command="Lower")
            sendOrder(duration, command="Raise")

            x = random.randrange(3)
            if(x == 0):
                sendOrder(duration, command="Rock")
                print("rock")
                
            elif x == 1:
                sendOrder(duration, command="Paper")
                print("paper")
                
            elif x == 2:
                sendOrder(duration, command="Cissor")
                print("cissors")
        if(i == 'r'):
            sendOrder(10, command="Rock")
            print("rock")
        if(i == 'p'):
            sendOrder(10, command="Paper")
            print("paper")
        if(i == 'c'):
            sendOrder(10, command="Cissor")
            print("cissors")

        if(i == 'q'):
            sendOrder(10,command="Park")
            # while manager.manager_thread.is_alive():
            #     continue
            #manager.manager_thread.join()
            


#rpsdemo()
betterrps()
# sendOrder(0,command="Park")
