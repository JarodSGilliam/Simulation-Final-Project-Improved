"""
circling.py
By: Jarod Gilliam

This program pings a message around in a circle between n logical processes where n is a number given by the user.


Controls:
 For all programs:
  -p VALUE = VALUE is the number of logical processes the simulation will use
  -s VALUE = VALUE indicates the end of simulation time
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
parser.add_argument('-p', action="store", dest="NUMBER_OF_LPS",default=5,type=int)
parser.add_argument('-s', action="store", dest="SIM_LENGTH",default=100,type=int)
parser.add_argument('-f', action="store_true", dest="STATIC_LATENCY",default=False)
parser.add_argument('-k', action="store", dest="LATENCY_LIMIT",default=5, type=int)
parser.add_argument('-r', action="store", dest="SEED",default=random.randint(1,310921094098), type=int)
args = parser.parse_args()


#Variables
bounces = 0
caravanCount = 0

#More setup
random.seed(args.SEED)

#real life data
names = ["a", "b", "c", "d", "e", "f", "g"]



#The classes:
class truck_stop:
    #is an object
    def __init__(self, id): #ping's initilization (Iproc)
        self.id = id
        self.name = names[id]
        self.trucks = []
        self.caravans = []
        self.drivers = []
        self.extraDrivers = False
        return
        #print("ping is initilized")
        
    def receiveMessage(self, message): #ping's running thing (Proc)
        self.trucks.append(message)
        for i in range(len(self.caravans)):
            print(self.caravans[i][0].name)
        temp = []
        temp.append(message)
        self.caravans.append(temp)
        if (len(self.trucks) == 4):
            print(4)
            print(self.trucks.pop(0).name)
        newTarget = message.target + 1
        if (newTarget == args.NUMBER_OF_LPS):
            newTarget = 0
        if (args.STATIC_LATENCY):   
            API.sendMessage(API.time + args.LATENCY_LIMIT, "circle" + str(newTarget), newTarget, "") #args.LATENCY_LIMIT
        else:
            API.sendMessage(API.time + random.randint(1, args.LATENCY_LIMIT), "circle" + str(newTarget), newTarget, "") #args.LATENCY_LIMIT
        global bounces
        bounces += 1
        print("Message received by " + self.name + "!")
    
    def arival(self, caravan, currentTime):
        self.driver.apend(caravan.getDriver())
        addEvent(event((currentTime + driver.getWaitTime()), "driverReady", self.id, None))
        n = caravan.getTrucks()
        for i in range(len(n)):
            found = False
            nextTarget = n[i].getNextTarget()
            for a in range(len(self.caravans)):
                if (nextTarget == self.caravans[a].getTarget):
                    self.caravans[a].append(n[i])
                    found = True
            if not(found):
                newCaravan = caravan(a[i])
                global truckWaitAmount
                addEvent(event((currentTime + truckWaitAmount), "truckReady", self.id, newCaravan.getId()))
                self.caravans.append(newCaravan, nextTarget, currentTime)
        print("esdfgj")


        del caravan
    
    def caravanReady(self):
        
        return

    
    def destructor(self): #ping's destructor (Fproc)
        return
        #print("done")


class caravan:
    def __init__(self, truck, target, formationTime):
        self.trucks = []
        self.trucks.append(truck)
        self.driver = None
        self.target = target
        self.formationTime = formationTime
        global caravanCount
        caravanCount = caravanCount + 1
        self.id = caravanCount
        self.ready = False
    
    def addTruck(self, truck):
        self.trucks.append(truck)
    
    def addDriver(self, driver):
        self.driver = driver
    
    def getTrucks(self):
        return self.trucks
    
    def getDriver(self):
        return self.driver
    
    def getTarget(self):
        return self.target
    
    def getFormTime(self):
        return self.formationTime
    
    def getId(self):
        return self.id
    
    def destructor(self):
        return



#RUNNING

#Prepping the Kernal
print("Working...")
LPs = []
for i in range(args.NUMBER_OF_LPS):
    LPs.append(truck_stop(i))
API.initialize(LPs, args.SIM_LENGTH)

API.sendMessage(1, "circle0", 0, "")
bounces += 1


#Running the Kernal
API.executeKernal(False)
#By here, Kernal has completed
print("Done!")

#Wrapping up
API.finalize()
print("The number of trips between between logical processes: " + str(bounces))


#DONE
