import queue
import collections
import socketserver
import socket
import pickle
import Robotarm
import threading
from Robotarm import Order

class SocketHandler(socketserver.StreamRequestHandler):
    orderManager = None
    def handle(self):
        data = self.rfile.readline()
        pickle.loads(data)
        self.orderManager.recievedOrders.put(data)

class ServerHandler(threading.Thread):
    def __init__(self, orderManager):
        super().__init__(self)
        self.orderManager = orderManager

    def run(self):
        self.socket = socketserver.TCPServer(('localhost',5000),SocketHandler)
        self.clientSocket = None
        self.socket.serve_forever()
    
class OrderManager:
    orderDict = {
        "OrderId":0, #unique id given to each order for modification
        "TargetPosition":[], #array of 6 angles as a target. exclusive with command
        "AnimationDuration": 0, #duration of the animation in deciseconds
        "InsertionMode":"Front","Interrupt" #Adds the order to the front of the queue to be executed after the current order
        "Command":"Park/Hold" #park or hold position after order. exclusive with targetposition
        }
    responseDict = {
        "OrderId":0,
        "Status":"Queued/Running/Done",
        "Error":"Message"
    }
    

    def __init__(self):
        self.orderQueue = collections.deque()
        self.runningOrder = None
        self.recievedOrders = queue.Queue()
        SocketHandler.orderManager = self
        serverThread = ServerHandler(self)
        serverThread.run()
        self.manageOrders()

    def manageOrders(self):
        while True:    
            self.processIncomingOrders()
            
    def manageRunningOrder(self):
        if self.runningOrder != None:
            if not self.runningOrder.isAlive():
                self.runningOrder = None
        elif self.orderQueue:
            self.runningOrder = self.orderQueue.popleft()
        

            


    def processIncomingOrders(self):
        while not self.recievedOrders.empty():
            order = self.recievedOrders.get()
            if "TargetPosition" in order and "AnimationDuration" in order:
                orderThread = Order(order["TargetPosition"],order["AnimationDuration"])
                self.orderQueue.append(orderThread)
            
        return order
                



    def getInsertionMode(self, order):
        if "InsertionMode" in order:
            interrupt=False
            insertFront = False
            if order["InsertionMode"] == "First":
                insertFront = True 
            if order["InsertionMode"] == "Interrupt":
                interrupt = True
        return insertFront, interrupt

                

            
            #process message

            #update queue/running thread
    


orderManager = OrderManager()
    