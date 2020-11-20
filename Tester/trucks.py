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
parser.add_argument('-s', action="store", dest="NUMBER_OF_STOPS",default=5,type=int)
parser.add_argument('-t', action="store", dest="NUMBER_OF_TRUCKS",default=500,type=int)
parser.add_argument('-l', action="store", dest="SIM_LENGTH",default=100,type=int)
parser.add_argument('-f', action="store_true", dest="STATIC_LATENCY",default=False)
parser.add_argument('-k', action="store", dest="LATENCY_LIMIT",default=5, type=int)
parser.add_argument('-r', action="store", dest="SEED",default=random.randint(1,310921094098), type=int)
args = parser.parse_args()


#Variables
bounces = 0
caravanCount = 0
truckCount = 0

arrives = 0
leaves = 0

#More setup
random.seed(args.SEED)

#real life data
names = ["a", "b", "c", "d", "e", "f", "g"]



#The classes:
class truck_stop:
    #is an object
    def __init__(self, id): #ping's initilization (Iproc)
        self.id = id
        self.trucks = []
        return
        #print("ping is initilized")
        
    # def receiveMessage(self, message): #ping's running thing (Proc)
    #     newTarget = message.target + 1
    #     if (newTarget == args.NUMBER_OF_LPS):
    #         newTarget = 0
    #     if (args.STATIC_LATENCY):   
    #         API.sendMessage(API.time + args.LATENCY_LIMIT, "circle" + str(newTarget), newTarget, "") #args.LATENCY_LIMIT
    #     else:
    #         API.sendMessage(API.time + random.randint(1, args.LATENCY_LIMIT), "circle" + str(newTarget), newTarget, "") #args.LATENCY_LIMIT
    #     global bounces
    #     bounces += 1
    #     print(self.id)
    
    def executeEvent(self, event):
        if (event.getType() == "arrive"):
            # print(event.getPayload().getId())
            self.arrive(event.getPayload())
            return
        elif (event.getType() == "leave"):
            self.leave(event.getPayload())
            return
        else:
            print(event.getType())
    
    def leave(self, truckId):
        truck = None
        for i in range(len(self.trucks)):
            if (self.trucks[i].getId() == truckId):
                truck = self.trucks.pop(i)
                break
        if (truck == None):
            print("Tried to remove truck that doesn't exist")
            return
        API.addEvent(API.time + getLatency(), "arrive", truck.getNextTarget(), truck)
        # print("Truck " + str(truckId) + " left " + str(self.id) + ". (" + str(len(self.trucks)) + " remaining)")
        global leaves
        leaves = leaves + 1
    
    def arrive(self, truck):
        waitTime = truck.getWaitTime
        self.trucks.append(truck)
        # print(self.trucks[0].getId())
        API.addEvent(API.time + getLatency(), "leave", self.id, truck.getId())
        # print("Truck " + str(truck.getId()) + " arrived at " + str(self.id) + ".")
        global arrives
        arrives = arrives + 1

    def destructor(self): #ping's destructor (Fproc)
        return
        #print("done")

def getLatency():
    if (args.STATIC_LATENCY):
        return random.randint(1, args.LATENCY_LIMIT)
    else:
        return args.LATENCY_LIMIT

def travelTime(thisStop, nextStop):
    times = [[1, 2, 3, 4, 5], []]
    return random.randint(1, args.LATENCY_LIMIT)



class truck():
    def __init__(self):
        global truckCount
        truckCount += 1
        self.id = truckCount
        self.truckTarget = []
        for i in range(100):
            self.truckTarget.append(random.randint(0, 4))
        self.waitTime = 5
    
    def getId(self):
        return self.id
    
    def getNextTarget(self):
        return self.truckTarget.pop(0)
    
    def getWaitTime(self):
        return self.waitTime


#RUNNING

#Prepping the Kernal
print("Working...")
LPs = []
for i in range(args.NUMBER_OF_STOPS):
    LPs.append(truck_stop(i))
API.initialize(LPs, args.SIM_LENGTH)

# API.sendMessage(1, "circle0", 0, "")
for i in range(args.NUMBER_OF_TRUCKS):
    API.addEvent(1, "arrive", random.randint(0, 4), truck())
bounces += 1


#Running the Kernal
API.executeKernal(False)
#By here, Kernal has completed
print("Done!")

#Wrapping up
extra = API.finalize()
# print("The number of trips between between logical processes: " + str(bounces))
print("Arrives = " + str(arrives) + "\nLeaves = " + str(leaves))


#DONE
