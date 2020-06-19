# robotarm
This code is used to controll a robot arm consisting of 6 180 degree servo's, controlled through a PCA9685 servo controller attatched to a Raspberry Pi.
It provides multiprocessed reception of orders via network, managing running orders and execution of orders.
The angles of the servo's that are needed are seperated from the actual servo angles, as determined by an array.

```angleTranslation = [[90,1],[90,1],[130,1],[40,1],[90,1],[0,1]]```

The first values are the servo angles that represent an input of 0, the second values are the direction of the translation, +1 or -1.

You can start the program by running OrderManager.py. You can use positionconfig2.py to quickly configure arrays of angles, or preform calibration.

You can also circumvent the network for testing by adding orders to the orderqueue directly.

The code is currently setup for a working rock-paper-cissors demo, which you can see in test.py
