"""
trucks.py
By: Jarod Gilliam

This program is designed to simulate trucks moving around.


Controls:
  -s VALUE = VALUE is the number truck stops
  -t VALUE = VALUE is the number of active trucks
  -l VALUE = VALUE indicates the end of simulation time
  -f       = fixed latency between logical processes (will be the value of -k (default or set) if -f is given)
  -k VALUE = VALUE is the upper limit of latency between logical processes
  -r VALUE = the seed of the random amount of latency between logical processes (does nothing when -f is given aka the latency is fixed)
  -p       = print extra information
  -i VALUE = VALUE determines the average number of truck stops a truck in the simulation will pass through (one way)
  -c       = randomizes the time the inital trucks are sent off
  -d VALUE = VALUE is the number of drivers in the simulation
  -m VALUE = VALUE is the maxumum length a caravan is aloud to be
  -local VALUE = VALUE is the number of drivers that start at each truck stop
  NOTE: The system is designed for realistic VALUEs. Non realistic VALUEs (like negative VALUEs) may break the system.

Return:
 This outputs statistics that can be used to discover the usefulness and/or efficiency of the system as a whole or the individual setting programmed in using the above command line arguments.
"""


#SET UP
#Offical imports
import argparse
import random
import math
import os
import sys

#My imports
import API
import TruckStop

#Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', action="store", dest="NUMBER_OF_STOPS",default=5,type=int)
parser.add_argument('-t', action="store", dest="NUMBER_OF_TRUCKS",default=1000,type=int)
parser.add_argument('-l', action="store", dest="SIM_LENGTH",default=1440,type=int)
parser.add_argument('-f', action="store_true", dest="STATIC_LATENCY",default=False)
parser.add_argument('-k', action="store", dest="LATENCY_LIMIT",default=5, type=int)
parser.add_argument('-r', action="store", dest="SEED",default=random.randint(1,310921094098), type=int)
parser.add_argument('-p', action="store_false", dest="PRINT",default=True)
parser.add_argument('-i', action="store", dest="STOPS_PER_TRUCK", default=7, type=int)
parser.add_argument('-c', action="store_false", dest="TIMING", default=False)
parser.add_argument('-d', action="store", dest="DRIVERS",default=200, type=int)
parser.add_argument('-m', action="store", dest="MAX_CARAVAN_LENGTH",default=100000, type=int)
parser.add_argument('-local', action="store", dest="LOCALIZED_DRIVERS", default=0, type=int)
parser.add_argument('-data', action="store", dest="TIMES_FILE", default=os.path.join(sys.path[0], "locations.txt"), type=str) #"C:\\Users\\jgill\\3D Objects\\Coding\\NEW\\"
parser.add_argument('-config', action="store", dest="CONFIGURATION_FILE", default=os.path.join(sys.path[0], "config.txt"), type=str) #"C:\\Users\\jgill\\3D Objects\\Coding\\NEW\\"
parser.add_argument('-verbose', action="store_true", dest="VERBOSE", default=False)
parser.add_argument('--verbose', action="store_true", dest="VERY_VERBOSE", default=False)
args = parser.parse_args()

#Variables
STOPCOUNT = args.NUMBER_OF_STOPS
TRUCKCOUNT = args.NUMBER_OF_TRUCKS
SIMLENGTH = args.SIM_LENGTH
DRIVERCOUNT = args.DRIVERS
CARAVANMAXLENGTH = args.MAX_CARAVAN_LENGTH
SEED = args.SEED
PRINT = args.PRINT
STATICLATENCY = args.STATIC_LATENCY
LATENCYLIMIT = args.LATENCY_LIMIT
STOPSPERTRUCK = args.STOPS_PER_TRUCK
TIMING = args.TIMING
LOCALIZEDDRIVERS = args.LOCALIZED_DRIVERS
TRAVELTIMEFILE = args.TIMES_FILE
CARAVANCOUNT = 0


ownsTruck = False

if (args.VERBOSE):
    print("eh")
if (args.VERY_VERBOSE):
    print("very")

#Stats
trucksTimeTaken = []
outgoingCaravansLength = []
outgoingCaravansWaitTime = []
leftOverTrucks = 0
driverready = 0
truckDeleted = 0
arrives = 0
leaves = 0

#More setup
random.seed(args.SEED)


#getting configuration information
try:
    configFile = open(args.CONFIGURATION_FILE, "r")
except:
    print("Error:\n The configuration file does not exist")
    exit(0)
travelTimes = []
for i in configFile:
    temp = []
    temp = i.split()
    temp[0] = temp[0][0:-1]
    if (len(temp) == 1):
        continue
    if (temp[0] == "NUMBER_OF_STOPS"):
        STOPCOUNT = temp[1]
    elif (temp[0] == "NUMBER_OF_TRUCKS"):
        TRUCKCOUNT = temp[1]
    elif (temp[0] == "SIM_LENGTH"):
        SIMLENGTH = temp[1]
    elif (temp[0] == "STATIC_LATENCY"):
        STATICLATENCY = temp[1]
    elif (temp[0] == "LATENCY_LIMIT"):
        LATENCYLIMIT = temp[1]
    elif (temp[0] == "SEED"):
        SEED = temp[1]
    elif (temp[0] == "PRINT"):
        PRINT = temp[1]
    elif (temp[0] == "STOPS_PER_TRUCK"):
        STOPSPERTRUCK = temp[1]
    elif (temp[0] == "TIMING"):
        TIMING = temp[1]
    elif (temp[0] == "DRIVERS"):
        DRIVERCOUNT = temp[1]
    elif (temp[0] == "MAX_CARAVAN_LENGTH"):
        CARAVANMAXLENGTH = temp[1]
    elif (temp[0] == "LOCALIZED_DRIVERS"):
        LOCALIZEDDRIVERS = temp[1]
    elif (temp[0] == "TIMES_FILE"):
        output = ""
        for i in temp:
            if (i != "TIMES_FILE"):
                output += i + " "
        travelTimesFile = output.strip()
    else:
        print("Error:\n The configuration file is not set up correctly")
        exit(0)
    # print(temp)
configFile.close()
print(travelTimes)
print(TRAVELTIMEFILE)
print(TRUCKCOUNT)

#getting real life data
if (args.TIMES_FILE != ""):
    print("AHHHH")
    TRAVELTIMEFILE = args.TIMES_FILE
try:
    travelTimesFile = open(TRAVELTIMEFILE, "r")
except:
    print("Error:\n The data file does not exist")
    exit(0)
travelTimes = []
for i in travelTimesFile:
    temp = []
    for a in i.split():
        if a.isdigit():
            temp.append(a);
        else:
            print("Error:\n Inputted file is not compatable")
            exit(0)
    travelTimes.append(temp)
travelTimesFile.close()
print(travelTimes)

print(TRAVELTIMEFILE)
exit(0)
#The classes:
# truckStop = TruckStop.truck_stop(1)
# exit(0)
# travelTimesFile = open(args.TIMESFILE, "r")
# travelTimes = []
# for i in travelTimesFile:
#     temp = []
#     for a in i.split():
#         if a.isdigit():
#             temp.append(a);
#         else:
#             print("Error:\n Inputted file is not compatable")
#             exit(0)
#     travelTimes.append(temp)

# truck stop class
class truck_stop:
    def __init__(self, id):
        self.id = id
        self.trucks = []
        self.drivers = []
        self.caravans = []
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
    
    #Handels when a caravan leaves a truck stop
    def leave(self, driverId):
        if (len(self.caravans) < 1):
            API.addEvent(API.time + 1, "leave", self.id, driverId)
            global driverready
            driverready += 1
            return
        driver = None
        for i in range(len(self.drivers)):
            if self.drivers[i].id == driverId:
                driver = self.drivers.pop(i)
                break
        if (driver == None):
            print("Error: Tried to get a driver that is not here")
        self.caravans.sort()
        outgoingCaravan = self.caravans.pop(0)

        if (args.LOCALIZEDDRIVERS > 0):
            for i in range(len(self.caravans)):
                if (driver.possibleSpots.count(self.caravans[i].destination) == 0):
                    API.addEvent(API.time + 1, "leave", self.id, driverId)
                    driverready += 1
                    self.drivers.append(driver)
                    return
            
        global outgoingCaravansLength, outgoingCaravansWaitTime
        outgoingCaravansLength.append(len(outgoingCaravan.trucks))
        outgoingCaravansWaitTime.append(API.time - outgoingCaravan.creationTime)
        outgoingCaravan.addDriver(driver)
        caravanId = outgoingCaravan.id #for testing
        API.addEvent(API.time + travelTimeAmount(self.id, outgoingCaravan.destination), "arrive", outgoingCaravan.destination, outgoingCaravan)
        global leaves #for testing
        leaves += 1 #for testing
        if (args.PRINT == True):
            print("caravan " + str(caravanId) + " with length " + str(len(outgoingCaravan)) + " just left from " + str(self.id)) #for testing

    #Handels when a caravan arrives at a truck stop
    def arrive(self, caravan):
        caravanDriver = caravan.takeDriver()
        caravanLen = len(caravan) #for testing
        if (caravanDriver == False):
            print("Error: Caravan arrived with no driver")
            return
        API.addEvent(API.time + caravanDriver.wait, "leave", self.id, caravanDriver.id)
        self.drivers.append(caravanDriver)
        for i in range(len(caravan)):
            truck = caravan.takeNextTruck()
            target = truck.getNextTarget()
            if (target == None):
                del truck
                global truckDeleted
                truckDeleted += 1
                global trucksTimeTaken
                trucksTimeTaken.append(API.time)
            else:
                self.addToCaravan(truck, target)
        caravanId = caravan.id #for testing
        if (len(caravan) != 0):
            print("Trucks left in caravan at deletion")
        del caravan
        for i in range(len(self.drivers)):
            if (self.drivers[i].ready):
                API.addEvent(API.time, "leave", self.id, self.drivers[i].id)
        global arrives #for testing
        arrives += 1 #for testing
        if (args.PRINT == True):
            print("caravan " + str(caravanId) + " with length " + str(caravanLen) + " just arrived at " + str(self.id)) #for testing
    
    #Adds a truck to a caravan
    def addToCaravan(self, truck, target):
        for i in range(len(self.caravans)):
            if (self.caravans[i].destination == target):
                self.caravans[i].addTruck(truck)
                return
        newCaravan = caravan(API.time)
        newCaravan.addTruck(truck, target)
        self.caravans.append(newCaravan)

    def destructor(self):
        global leftOverTrucks
        for i in range(len(self.caravans)):
            for a in range(len(self.caravans[i].trucks)):
                leftOverTrucks += 1
        return

#Gets a random amount of time for a driver to wait at a truck stop
def getLatency():
    if (args.STATIC_LATENCY):
        return random.randint(1, args.LATENCY_LIMIT)
    else:
        return args.LATENCY_LIMIT

#Find the amount of time it takes to get from truck stop "start" to truck stop "end"
def travelTimeAmount(start, end):
    for i in range(len(travelTimes)):
        if start == travelTimes[i][0] and end == travelTimes[i][1]:
            return travelTimes[i][2]
        if start == travelTimes[i][1] and end == travelTimes[i][0]:
            return travelTimes[i][2]
    print("time not found from " + str(start) + " to " + str(end))
    return -1

#Find a random stop that can be traved to from the truck stop "start" and make sure running this multiple times does not just bouncing back and forth between two truck stops
def findRandNextStop(start, previous):
    possibleNextSpots = []
    for i in range(len(travelTimes)):
        if start == travelTimes[i][0] and previous != travelTimes[i][1]:
            possibleNextSpots.append(travelTimes[i][1])
        if start == travelTimes[i][1] and previous != travelTimes[i][0]:
            possibleNextSpots.append(travelTimes[i][0])
    if (len(possibleNextSpots) == 0):
        for i in range(len(travelTimes)):
            if start == travelTimes[i][0]:
                possibleNextSpots.append(travelTimes[i][1])
            if start == travelTimes[i][1]:
                possibleNextSpots.append(travelTimes[i][0])
    return possibleNextSpots[random.randint(0, len(possibleNextSpots)-1)]

# gets the time from any truck stop to any other
def travelTime(thisStop, nextStop):
    times = [[1, 2, 3, 4, 5], []]
    return random.randint(1, args.LATENCY_LIMIT)


# truck class
class truck():
    def __init__(self, driver = None, start = None, nextStop = None):
        global TRUCKCOUNT
        TRUCKCOUNT += 1
        self.id = TRUCKCOUNT
        self.truckTarget = [nextStop]
        self.truckTarget.append(findRandNextStop(self.truckTarget[-1], -1))
        for i in range(random.randint(args.STOPSPERTRUCK-2,args.STOPSPERTRUCK+2)):
            self.truckTarget.append(findRandNextStop(self.truckTarget[-1], self.truckTarget[-2]))
        for i in range(len(self.truckTarget)-2, -1, -1):
            self.truckTarget.append(self.truckTarget[i])
        self.truckTarget.append(start)
        self.waitTime = 5
        self.driver = driver
    
    def getId(self):
        return self.id
    
    def getNextTarget(self):
        if len(self.truckTarget) == 0:
            return None
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


# driver class
class driver():
    def __init__(self, truckId = None, limitedStops = False, startingStop = -1):
        global driverCount
        driverCount += 1
        self.id = driverCount
        if (truckId != None):
            global ownsTruck
            self.hasSpecificTruck = ownsTruck
            self.truck = truckId
        self.wait = math.floor(30/(args.STOPSPERTRUCK+2)) #args.LATENCY_LIMIT + 5
        self.ready = False
        self.possibleSpots = [startingStop]
        if (limitedStops):
            global travelTimes
            for i in range(len(travelTimes)):
                if startingStop == travelTimes[i][0]:
                    self.possibleSpots.append(travelTimes[i][1])
                if startingStop == travelTimes[i][1]:
                    self.possibleSpots.append(travelTimes[i][0])
        return
    
    def getId(self):
        return self.id
    
    def getTruck(self):
        if (self.hasSpecificTruck):
            return self.truck
        else:
            return False

# caravan class
class caravan():
    def __init__(self, creationTime, givenId = None):
        if (givenId != None):
            self.id = givenId
            return
        global caravanCount
        caravanCount += 1
        self.id = caravanCount
        self.trucks = []
        self.destination = None
        self.driver = None
        self.creationTime = creationTime

    def __len__(self):
        return len(self.trucks)

    def __lt__(self, other):
        return self.creationTime < other.creationTime
    
    def addTruck(self, truck, destination = None):
        self.trucks.append(truck)
        if (destination != None):
            self.destination = destination
        return
    
    def addDriver(self, driver):
        if (self.driver == None):
            self.driver = driver
            return True
        return False
    
    def takeDriver(self):
        if (self.driver == None):
            return False
        output = self.driver
        self.driver = None
        return output
    
    def takeNextTruck(self):
        if (len(self.trucks) > 0):
            return self.trucks.pop(0)
        return None
    
    def waitTime(self, currentTime):
        self.creationTime 



#RUNNING:
#Prepping the Kernal
print("Working...")
drivers = []
for i in range(args.DRIVERS+1): #args.NUMBER_OF_TRUCKS
    drivers.append(driver())

numberOfDrivers = args.DRIVERS
#Generate all Truck Stops
TruckStops = []
for i in range(140):
    TruckStops.append(truck_stop(i))
    if (args.LOCALIZEDDRIVERS > 0):
        for a in range(args.LOCALIZEDDRIVERS):
            TruckStops[i].drivers.append(driver(limitedStops=True, startingStop=i))
API.initialize(TruckStops, args.SIM_LENGTH)

caravans = int(args.DRIVERS)
for i in range(caravans):
    tempCaravan = caravan(0)
    startingStop = 130 + random.randint(1,5)
    nextStop = findRandNextStop(startingStop, -1)
    for i in range(math.floor(args.NUMBER_OF_TRUCKS/args.DRIVERS)):
        tempCaravan.addTruck(truck(start=startingStop, nextStop=nextStop))
    tempCaravan.addDriver(drivers[i])
    if (args.PRINT == True):
        print("caravan " + str(tempCaravan.id) + " of length " + str(len(tempCaravan)) + " was just created")
    if (args.TIMING):
        API.addEvent(random.randInt(1, args.SIM_LENGTH/2), "arrive", startingStop, tempCaravan)
    else:
        API.addEvent(1, "arrive", startingStop, tempCaravan)


#Running the Kernal
API.executeKernal(False)
#By here, Kernal has completed
print("Done!")

#Wrapping up
extra = API.finalize()
print("time spent with drivers ready with no caravan = " + str(driverready))
print("trucks who compteted their routes = " + str(truckDeleted))
print("average caravan length = " + str(round((sum(outgoingCaravansLength)/len(outgoingCaravansLength))*10)/10))
print("average time it takes to deliver a truck = " + str(round((sum(trucksTimeTaken)/len(trucksTimeTaken))*100)/100))
print("average caravan wait time = " + str(round((sum(outgoingCaravansWaitTime)/len(outgoingCaravansWaitTime))*100)/100))
print("average time wasted = " + str(round(((sum(outgoingCaravansWaitTime)/len(outgoingCaravansWaitTime))*(args.STOPSPERTRUCK+2))*100)/100))
print("time wasted percentage = " + str(round(((sum(outgoingCaravansWaitTime)/len(outgoingCaravansWaitTime))*(args.STOPSPERTRUCK+2))/(sum(trucksTimeTaken)/len(trucksTimeTaken))*10000)/100))
print("trucks stranded at simulation end = " + str(leftOverTrucks))
print("Arrives = " + str(arrives) + "\nLeaves = " + str(leaves))


#DONE
