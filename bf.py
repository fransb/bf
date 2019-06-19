import argparse
from decimal import *
from operator import itemgetter

def sortDist(val): 
    return float(val["distance"])
def parseLine(line, refLat, refLong, file):

def parseLine(line, refLat, refLong):
    tacobject = dict()
    id = ""
    long = Decimal(0.0)
    lat = Decimal(0.0)
    alt = Decimal(0.0)
    type = ""
    name = ""
    color = ""
    coalition = ""
    country = ""
    group = ""
    status = "alive"
    
    for part in line.rstrip().split(","):
        if "T=" in part:
            long = Decimal(part.split("|")[0].replace("T=",""))+refLong
            lat = Decimal(part.split("|")[1])+refLat
            alt = part.split("|")[2]
        elif "Type=" in part:
            type = part.replace("Type=","")
        elif "Name=" in part:
            name = part.replace("Name=","")
        elif "Color=" in part:
            color = part.replace("Color=","")
        elif "Coalition=" in part:
            coalition = part.replace("Coalition=","")
        elif "Country=" in part:
            country = part.replace("Country=","")
        elif "Group=" in part:
            group = part.replace("Group=","")
        elif not "=" in part :
            id = part.rstrip()
    tacobject["id"] = id + file
    tacobject["long"] = long
    tacobject["lat"] = lat
    tacobject["alt"] = alt
    tacobject["type"] = type
    tacobject["name"] = name
    tacobject["color"] = color
    tacobject["coalition"] = coalition
    tacobject["country"] = country
    tacobject["group"] = group
    tacobject["status"] = status
    return tacobject

def readFile(file, targets):
    linenumber = 0
    fileStarted = False
    refLong = Decimal(0.00)
    refLat = Decimal(0.00)
    time = 0
    print("Reading File: " + file)
    with open(file) as f:
        for line in f:
            linenumber = linenumber + 1
            if line[0] == "#":
                fileStarted = True
                time = Decimal(line[1:])
            elif fileStarted:
                split_line = line.split(",")
                id = split_line[0].rstrip()
                if id[0] == "-":
                    targets[id[1:]+file]["status"]="dead"
                    #TODO delete tecical object
                elif id == "0":
                    pass
                    #TODO handle special object
                elif not id+file in targets:
                    targets[id+file] = parseLine(line, refLat, refLong, file)
            elif "ReferenceLongitude" in line:
                refLong = Decimal(line.split("=")[1])
            elif "ReferenceLatitude" in line:
                refLat = Decimal(line.split("=")[1])

parser = argparse.ArgumentParser(description='Get targets')
parser.add_argument('--tacviewFile', metavar='tacviewFile', nargs='*', default=['H:/Tacview.txt.acmi',
                                                                                'H:/1.acmi',
                                                                                'H:/2.acmi',
                                                                                'H:/3.acmi',
                                                                                'H:/4.acmi',
                                                                                'H:/5.acmi'],
                    help='unzipped tacview file')
args = parser.parse_args()
print(args.tacviewFile)
for file in args.tacviewFile:
    readFile(file, targets)
    
linenumber = 0
fileStarted = False
refLong = Decimal(0.00)
refLat = Decimal(0.00)
time = 0
with open(args.tacviewFile) as f:
    for line in f:
        linenumber = linenumber + 1
        if line[0] == "#":
            fileStarted = True
            time = Decimal(line[1:])
        elif fileStarted:
            split_line = line.split(",")
            id = split_line[0]
            if id[0] == "-":
                pass
                #TODO delete tecical object
            elif id == "0":
                pass
                #TODO handle special object
            elif not id in targets:
                targets[id] = parseLine(line, refLat, refLong)
        elif "ReferenceLongitude" in line:
            refLong = Decimal(line.split("=")[1])
        elif "ReferenceLatitude" in line:
            refLat = Decimal(line.split("=")[1])
    
longmax = Decimal(0.0)
longmin = Decimal(90.0)
latmax = Decimal(0.0)
latmin = Decimal(90.0)
for target in targets.values():
    if longmax < target["long"]:
        longmax = target["long"]
    if latmax < target["lat"]:
        latmax = target["lat"]
    if longmin > target["long"]:
        longmin = target["long"]
    if latmin > target["lat"]:
        latmin = target["lat"]
        #print(target)
newTarget = True
while newTarget :
    lat = Decimal(input("Enter latitude for target in format " + str(latmin) + "-" + str(latmax) + ": ").replace(",","."))
    long = Decimal(input("Enter longitude for target in format " + str(longmin) + "-" + str(longmax) + ": ").replace(",","."))
    targettype = input("Enter type a=all, aa=AntiAircraft, b=Building [aa]: ")
    if targettype == "":
        targettype = "aa"
    distanses = []
    for target in targets.values():
        if "Ground" in target["type"] or "Sea" in target["type"] :
            found = False
            if targettype == "a" :
                found = True
            elif "AntiAircraft" in target["type"] and targettype == "aa" :
                found = True
            elif "Building" in target["type"] and targettype == "b" :
                found = True
            if found :
                distance = ((target["lat"]-lat)**2+(target["long"]-long)**2).sqrt()
                target["distance"]=distance
                distanses.append(target)

    distanses.sort(key = sortDist)

    for distance in distanses:
        if distance["distance"] < Decimal(0.05):
            print(distance["status"]+", "+distance["type"]+", "+distance["name"]+", "+str(distance["lat"])+", "+str(distance["long"])+", "+str(distance["alt"])+" m, " + distance["group"]+", "+str(distance["distance"]))
    
    if input("New Target y/n: ") == "n":
        newTarget = False
