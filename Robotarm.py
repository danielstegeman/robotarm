from adafruit_servokit import ServoKit
import time
import threading

class Order:
    connectedServoAmount = 6
    #[[sevo angle set as 0, translation direction(-1,+1)]]
    angleTranslation = [[90,1],[0,1],[180,-1],[120,1],[90,1],[0,1]]
    kit = ServoKit(channels=16)
    
    def __init__(self,orderId,movementTarget,animationDuration):
        super().__init__()
        #self.parkArm()
        self.orderId = orderId
        self.TargetPosition = []
        self.interupt = False
        self.animationDuration = animationDuration
        self.movementTarget = movementTarget
        self.orderComplete = False

    def run(self):
        self.animateToPosition(self.movementTarget,self.animationDuration)
        
    def parkArm(self):
        parkAngles = [0,80,10,-90,0,80]
        for i in range(self.connectedServoAmount):
            self.kit.servo[i].angle = self.translateAngle(i,parkAngles[i])

    def translateAngle(self,index,angle):
        servoAngle= self.angleTranslation[index][0]+ angle*self.angleTranslation[index][1]
        return servoAngle

    def translateAngleArray(self,angleArray):
        servoAngleArray=[]
        for i in range(len(angleArray)):
            servoAngleArray.append(self.translateAngle(i,angleArray[i]))
        return servoAngleArray

    def setPosition(self, angleArray):
        for i in range(len(angleArray)):
            self.kit.servo[i].angle = self.translateAngle(i,angleArray[i])

    def getCurrentServoPositions(self):
        servoPositions =[]
        for i in range(self.connectedServoAmount):
            servoPositions.append(self.kit.servo[i].angle)
        return servoPositions

    def animateToPosition(self,targetAngleArray,animationDuration):
        servoTargets = self.translateAngleArray(targetAngleArray)
        currentPositions = self.getCurrentServoPositions()
        movementPerMs = []
        for i in range(len(servoTargets)):
            difference = servoTargets[i] - currentPositions[i]
            movementPerMs.append(difference/animationDuration)
        startTime = time.perf_counter()

        while (time.perf_counter()-startTime)*10<animationDuration:
            
            for j in range(len(movementPerMs)):
                self.kit.servo[j].angle=self.kit.servo[j].angle+movementPerMs[j]
            time.sleep(0.1)
        self.orderComplete = True
        print(f"Order {self.orderId} complete")
    
        
        
        
