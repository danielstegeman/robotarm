UseRobot = True

import queue
import collections
import socketserver
import socket
import pickle
import threading
if UseRobot:
    import Robotarm
    from Robotarm import Order
import multiprocessing
orderManager = None

HOST = 'localhost'
PORT = 0


class SocketHandler(socketserver.StreamRequestHandler):

    def handle(self):
        
        data = self.rfile.read()
        for splitData in data.split(b"|"):
            if len(splitData)>2:
                order = pickle.loads(splitData)
                self.server.orderManager.recievedOrders.put(order)
                print(order)

class ServerHandler(socketserver.TCPServer):
     def __init__(self, host_port_tuple, streamhandler, orderManager):
        super().__init__(host_port_tuple, streamhandler)
        self.allow_reuse_address = True
        self.orderManager = orderManager
        print(self.server_address)
        #self.allow_reuse_address = True
    
        
        
    
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
    
    commands={
        "Park" :[0,0,20,-10,0,70],
        "Rock":[0, 0, -40, 50, 0, 0],
        "Paper":[0, 0, -40, 50, -90, 45],
        "Cissor":[0, 0, -40, 50, 0, 55],
        "Raise":[0, 25, -50, 70, -80, 0],
        "Lower":[0, 0, -40, 50, -80, 0]

    }
    commands2={
        "Park" :[0,0,20,-10,0,70],
        "Rock":[0, 20, -50, 130, 0, 0],
        "Paper":[0, 20, -50, 130, -90, 45],
        "Cissor":[0, 20, -50, 130, 0, 55],
        "Raise":[0, 70, -50, 90, -80, 0],
        "Lower":[0, 20, -50, 130, -80, 0]
    }
    commands3={
        "Park" :[0,0,20,-10,0,70],
        "Rock":[0, 80, -50, 20, 0, 0],
        "Paper":[0, 80, -50, 20, -90, 45],
        "Cissor":[0, 80, -50, 20, 0, 55],
        "Raise":[0, 80, -50, 50, -80, 0],
        "Lower":[0, 80, -50, 20, -80, 0]
    }
#[0, 25, -50, 70, -80, 0]

    def __init__(self):
        self.commandDict = self.commands2
        self.orderQueue = collections.deque()
        self.runningOrder = None
        self.recievedOrders = queue.Queue()
        self.socket = ServerHandler((HOST,PORT),SocketHandler,self)
    
        self.clientSocket = None
        self.server_thread = threading.Thread(target=self.socket.serve_forever)
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()
        self.process = None
        if UseRobot:
            order = Order(0,[],0)
            order.parkArm()
        self.manager_thread = threading.Thread(target=self.manageOrders)
        self.manager_thread.daemon = True
        self.manager_thread.start()
        #self.manageOrders()

    def manageOrders(self):
        while True:
            if UseRobot:
                self.processIncomingOrders()
                self.manageRunningOrder()
            
    def manageRunningOrder(self):
        if self.runningOrder != None:
            if not self.process.is_alive():
                self.process.join()
                self.process = None
                self.runningOrder = None
        elif self.orderQueue:
            self.runningOrder = self.orderQueue.popleft()
            self.process = multiprocessing.Process(target=self.runningOrder.run)
            self.process.start()
        
        

    def processIncomingOrders(self):
        
        while not self.recievedOrders.empty():
            order = self.recievedOrders.get()
            if "AnimationDuration" in order:
                if "TargetPosition" in order:
                    orderThread = Order(order["OrderId"],order["TargetPosition"],order["AnimationDuration"])
                    self.orderQueue.append(orderThread)
                if "Command" in order:
                    if order["Command"] in self.commandDict:
                        orderThread = Order(order["OrderId"],self.commandDict[order["Command"]],order["AnimationDuration"])
                        self.orderQueue.append(orderThread)
       
                
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
    


manager = OrderManager()
    