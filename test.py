#import gpio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time
import enum
from Robotarm import RobotArm

kit = ServoKit(channels=16)

# parkAngles = [0,80,10,-90,0,80]
# target = [0,100,-110,0,45,0]
# robot = RobotArm()
kit.servo[2].angle = 100
print(kit.servo[2].angle)
# #robot.animateToPosition(target,20)
# robot.setPosition(target)
# #robot.animateToPosition(parkAngles,20)