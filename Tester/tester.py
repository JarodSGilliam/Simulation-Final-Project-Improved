import trucks

caravans = []

newCaravan = trucks.caravan(0)
newCaravan.addTruck(trucks.truck(trucks.driver()), 0)

caravans.append(newCaravan)

print("stuffs: " + str(newCaravan.trucks[0].getId()))

def addCaravan(time):
    newCaravan = trucks.caravan(time)
    newCaravan.addTruck(trucks.truck(trucks.driver()), 0)
    caravans.append(newCaravan)

addCaravan(32)
addCaravan(1)
addCaravan(31789)
addCaravan(32)
addCaravan(501)

caravans.sort()

for i in range(len(caravans)):
    print("stuffs 2: " + str(caravans[i].creationTime))
