"""
trucks.py
By: Jarod Gilliam

This program is designed to simulate trucks moving around.


Controls:
 For all programs:
  -s VALUE = VALUE is the number truck stops
  -t VALUE = VALUE is the number of active trucks
  -l VALUE = VALUE indicates the end of simulation time
  -f = fixed latency between logical processes (will be the value of -k (default or set) if -f is given)
  -k VALUE = VALUE is the upper limit of latency between logical processes
  -r VALUE = the seed of the random amount of latency between logical processes (does nothing when -f is given aka the latency is fixed)

Return:
 This outputs the number of times the message has been received by any of the logical processes.
"""


#SETTING UP

#Offical imports
import argparse
import random

#My imports
import API

#Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', action="store", dest="NUMBER_OF_STOPS",default=5,type=int)
parser.add_argument('-t', action="store", dest="NUMBER_OF_TRUCKS",default=500,type=int)
parser.add_argument('-l', action="store", dest="SIM_LENGTH",default=100,type=int)
parser.add_argument('-f', action="store_true", dest="STATIC_LATENCY",default=False)
parser.add_argument('-k', action="store", dest="LATENCY_LIMIT",default=5, type=int)
parser.add_argument('-r', action="store", dest="SEED",default=random.randint(1,310921094098), type=int)
args = parser.parse_args()
ownsTruck = False


#Variables
caravanCount = 0
truckCount = 0
driverCount = 0

arrives = 0
leaves = 0

#More setup
random.seed(args.SEED)

#real life data
names = ["a", "b", "c", "d", "e", "f", "g"]



#The classes:
class truck_stop:
    def __init__(self, id):
        self.id = id
        self.trucks = []
        self.drivers = []
        return
        
    def executeEvent(self, event):
        if (event.getType() == "arrive"):
            self.arrive(event.getPayload())
            return
        elif (event.getType() == "leave"):
            self.leave(event.getPayload())
            return
        else:
            print(event.getType())
    
    def leave(self, truckId):
        if (len(self.drivers) == 0):
            API.addEvent(API.time + 1, "leave", self.id, truckId)
            return
        truck = None
        for i in range(len(self.trucks)):
            if (self.trucks[i].getId() == truckId):
                truck = self.trucks.pop(i)
                break
        if (truck == None):
            print("Tried to remove truck that doesn't exist")
            return 
        truck.addDriver(self.drivers.pop(0))
        API.addEvent(API.time + getLatency(), "arrive", truck.getNextTarget(), truck)
        global leaves
        leaves = leaves + 1
        # if (self.id == 0):
            # print(len(self.drivers))
        # print("leave from " + str(self.id))

    
    def arrive(self, truck):
        waitTime = truck.getWaitTime()
        self.trucks.append(truck)
        API.addEvent(API.time + getLatency(), "leave", self.id, truck.getId())
        global arrives
        arrives = arrives + 1
        self.drivers.append(truck.takeDriver())
        # print("arrive at " + str(self.id))

    def destructor(self):
        return

def getLatency():
    if (args.STATIC_LATENCY):
        return random.randint(1, args.LATENCY_LIMIT)
    else:
        return args.LATENCY_LIMIT

def travelTime(thisStop, nextStop):
    times = [[1, 2, 3, 4, 5], []]
    return random.randint(1, args.LATENCY_LIMIT)



class truck():
    def __init__(self, driver):
        global truckCount
        truckCount += 1
        self.id = truckCount
        self.truckTarget = []
        for i in range(100):
            self.truckTarget.append(random.randint(0, 4))
        self.waitTime = 5
        self.driver = driver
    
    def getId(self):
        return self.id
    
    def getNextTarget(self):
        return self.truckTarget.pop(0)
    
    def getWaitTime(self):
        return self.waitTime
    
    def getDriver(self):
        return self.driver
    
    def takeDriver(self):
        if (self.driver == None):
            return False
        output = self.driver
        self.driver = None
        return output
    
    def addDriver(self, driver):
        if (self.driver == None):
            self.driver = driver
            return True
        else:
            return False
        

class driver():
    def __init__(self, truckId):
        global driverCount
        driverCount += 1
        self.id = driverCount
        global ownsTruck
        self.hasSpecificTruck = ownsTruck
        self.truck = truckId
        return
    
    def getId(self):
        return self.id
    
    def getTruck(self):
        if (self.hasSpecificTruck):
            return self.truck
        else:
            return False


#RUNNING

#Prepping the Kernal
print("Working...")
drivers = []
for i in range(args.NUMBER_OF_TRUCKS):
    drivers.append(driver())
LPs = []
for i in range(args.NUMBER_OF_STOPS):
    LPs.append(truck_stop(i))
API.initialize(LPs, args.SIM_LENGTH)

# API.sendMessage(1, "circle0", 0, "")
for i in range(args.NUMBER_OF_TRUCKS):
    API.addEvent(1, "arrive", random.randint(0, 4), truck(drivers[i]))


#Running the Kernal
API.executeKernal(False)
#By here, Kernal has completed
print("Done!")

#Wrapping up
extra = API.finalize()
# print("The number of trips between between logical processes: " + str(bounces))
print("Arrives = " + str(arrives) + "\nLeaves = " + str(leaves))


#DONE
