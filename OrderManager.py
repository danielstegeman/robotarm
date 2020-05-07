import queue
import collections
import socketserver
import socket
import pickle
class SocketHandler(socketserver.StreamRequestHandler):
    orderManager = None
    def handle(self):
        data = self.rfile.readline()
        pickle.loads(data)
        orderManager.recievedOrders.append(data)

class OrderManager:
    orderDict = {
        "OrderId":0, #unique id given to each order for modification
        "TargetPosition":[], #array of 6 angles as a target. exclusive with command
        "AnimationDuration": 0, #duration of the animation in deciseconds
        "InsertionMode":"Front", #Adds the order to the front of the queue to be executed after the current order
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
        self.recievedOrders = []
        self.clientSocket = None
        self.socket = socketserver.TCPServer(('localhost',5000),SocketHandler)
        SocketHandler.orderManager = self
        self.socket.serve_forever()

    def manageOrders(self):
        while True:
            #accept connection
            pass
                
            #check for recieved message
            
            #process message

            #update queue/running thread
    


orderManager = OrderManager()
    