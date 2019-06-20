import argparse
from decimal import *
from operator import itemgetter
import json
import zlib
import math
def printTarget(targets, long, lat, targettype, dead):
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
            if dead or target["status"] == "dead":
                found = False
            if found :
                distance = math.sqrt((target["lat"]-lat)**2+(target["long"]-long)**2)
                target["distance"]=distance
                distanses.append(target)

    distanses.sort(key = sortDist)
    closest = 0
    for distance in distanses:
        if (distance["distance"] < Decimal(0.1)) or closest < 20: 
            print(distance["status"]+", "+distance["type"]+", "+distance["name"]+", "+str(distance["lat"])+", "+str(distance["long"])+", "+str(distance["alt"])+" m, " + distance["group"]+", "+str(distance["distance"]))
            closest = closest + 1
def sortDist(val): 
    return float(val["distance"])
def parseLine(line, refLat, refLong, file):
    tacobject = dict()
    id = ""
    long = 0.0
    lat = 0.0
    alt = 0.0
    type = ""
    name = ""
    color = ""
    coalition = ""
    country = ""
    group = ""
    status = "alive"
    doPrint = False
    
    for part in line.rstrip().split(","):
        if "T=" in part:
            if not part.split("|")[0].replace("T=","") == "":
                long = float(part.split("|")[0].replace("T=",""))+refLong
            if not part.split("|")[1] == "":
                lat = float(part.split("|")[1])+refLat
            if not part.split("|")[2] == "":
                alt = float(part.split("|")[2])
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
    if doPrint:
        print(tacobject)
        print(line)
    
    return tacobject
def readFile(file, targets):
    linenumber = 0
    fileStarted = False
    refLong = 0.00
    refLat = 0.00
    time = 0
    print("Reading File: " + file)
    with open(file) as f:
        for line in f:
            linenumber = linenumber + 1
            if line[0] == "#":
                fileStarted = True
                time = line[1:]
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
                refLong = float(line.split("=")[1])
            elif "ReferenceLatitude" in line:
                refLat = float(line.split("=")[1])
parser = argparse.ArgumentParser(description='Get targets')
parser.add_argument('--tacviewFile', metavar='tacviewFile', nargs='*', default=['H:/Tacview.txt.acmi',
                                                                                #'H:/1.acmi',
                                                                                #'H:/2.acmi',
                                                                                #'H:/3.acmi',
                                                                                #'H:/4.acmi',
                                                                                #'H:/5.acmi'
                                                                                ],
                    help='unzipped tacview file')
parser.add_argument('--json', metavar='json', nargs='?', help='json')
parser.add_argument('-o', metavar='longitude', type=float, nargs='?', help='an integer for the longitude', default='56.223681')
parser.add_argument('-a', metavar='latitude', type=float, nargs='?', help='an integer for the latitude', default='27.131101')
parser.add_argument('-p', help='only arguments', action='store_true')
parser.add_argument('--target', default='a', const='a', nargs='?', choices=["a", "aa", "b"], help='list antiair, all, or building (default: %(default)s)')
parser.add_argument('--dead', help='print dead units')
parser.add_argument('--loop', dest='loop', action='store_true')
parser.add_argument('--no-loop', dest='loop', action='store_false')
parser.set_defaults(loop=False)
args = parser.parse_args()
targets = {}
print(args.json)
if args.json == None: 
    for file in args.tacviewFile:
        readFile(file, targets)
        with open('data.json', 'w') as f:  # writing JSON object
            json.dump(targets, f)
            original_data = open('data.json', 'rb').read()  
            compressed_data = zlib.compress(original_data, zlib.Z_BEST_COMPRESSION)
            f = open('data.json.compressed', 'wb')  
            f.write(compressed_data)  
            f.close()
else:
    try:
        json_file=open(args.json, "r")
        targets = json.load(json_file)
    except:
        compressed_file=open(args.json+".compressed", "rb")
        decompressed_data = zlib.decompress(compressed_file.read())
        targets = json.load(decompressed_data)#TODO something is broken


longmax = 0.0
longmin = 90.0
latmax = 0.0
latmin = 90.0
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
if not args.p:
    newTarget = True
    while newTarget :
        lat = float(input("Enter latitude for target in format " + str(latmin) + "-" + str(latmax) + ": ").replace(",","."))
        #lat = Decimal(27.1024)
        long = float(input("Enter longitude for target in format " + str(longmin) + "-" + str(longmax) + ": ").replace(",","."))
        #long = Decimal(56.1035)
        targettype = input("Enter type a=all, aa=AntiAircraft, b=Building [aa]: ")
        #targettype = "a"
        if targettype == "":
            targettype = "aa"
        printTarget(targets, long, lat, targettype, false)
        
        if input("New Target y/n: ") == "n":
            newTarget = False
else:
    dead=True
    if args.dead is None:
        dead=False
    printTarget(targets, args.o, args.a, args.target, dead)