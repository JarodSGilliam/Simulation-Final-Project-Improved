"""
API.py

The backend that allows the pingpong.py, circling.py, and phold to work.

Return:
 This will not return anything. Running it on its own will do nothing. It exists soley as support for the other three programs (and many others potentially).
"""

#SETUP
#imports
import queue
import random

#initial variables
q = queue.PriorityQueue()
time = 0
SIM_LENGTH = 31
#This contains all of the LPs which are generated in the file calling API, then stored here so they can be interacted with by the system
LPs = []

#This class represents a message and a payload (for futureproofing not really used in these three programs) and all other nessisary tags to make the system function
class message:
    def __init__(self, time, name, target, payload):
        self.time = time
        self.name = name
        self.target = target
        self.payload = payload

    def __lt__(self, other):
        return self.name < other.name

#A connection between the logical processors stored in the LPs array and the priority queue q built for abstraction's sake
def sendMessage(time, name, target, payload):
    global q
    q.put((time, message(time, name, target, payload)))


class event:
    def __init__(self, eventType, target, payload):
        self.type = eventType #leave, driver ready, truck ready, arrive
        self.target = target #a truckstop
        self.payload = payload #caravan (array of trucks), driver, caravan (array of trucks)
        self.tiebreaker = random.randint(0, 1000000)
    
    def getType(self):
        return self.type

    def getTarget(self) :
        return self.target
    
    def getPayload(self):
        return self.payload
    
    def __lt__(self, other):
        return self.tiebreaker < other.tiebreaker


def addEvent(time, eventType, location, payload):
    global q
    q.put((time, event(eventType, location, payload)))


#RUNNING THE PROGRAM
#Initializes everything
def initialize(array, length):
    #Getting the simulation's time limit calling program which gets it from the user
    global SIM_LENGTH
    SIM_LENGTH = length

    #Getting all of the LPs that have been created and storing them here so they can be run
    global LPs
    LPs = array


#The execution of the simulation in which the system continuously dequeues messages from the PriorityQueue and deals with them until 
def executeKernal(showqLength):
    ranTimes = 0
    global time
    lastTime = -1
    #The central loop of the program
    while (q.empty() == False):
        #Prints the lenght q (aka the number of active messages) at time t
        if (showqLength and (lastTime != time)):
            print("When time = " + str(time) + ", the number of active messages is " + str(q.qsize()))
            lastTime = time
        
        #Aquiring the next message from the queue
        qItem = q.get()
        event = qItem[1]

        #If time is up, then finnish the kernal's execution
        if (qItem[0] > SIM_LENGTH):
            q.put(qItem)
            return
        time = qItem[0]

        #Runs the event
        #Since the event can be diffrent based on what the LP does (ping's receiveMessage is very diffrent than p-hold's), the LP contains the code for this part, not API
        #Since the event scheduling may be diffrent depending on the simulation and the user's imputs it is also handled by the indiviudal LPs (stored in the LPs array)
        LPs[event.getTarget()].executeEvent(event)


#Deinitilizes everything and returns the number of messages that were scheduled but had not been received yet when execution time ran out
def finalize():
    #Counts the left over messages
    out = 0
    while (q.empty() == False):
        q.get()
        out += 1
    #Calls the constructors
    for i in LPs:
        i.destructor()
    #Returns the number of left over messages
    return out
