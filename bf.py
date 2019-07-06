import argparse
from decimal import *
from operator import itemgetter
import json
import zlib
import math
from tacticalObject import *
from latlongType import *

def printTarget(targets, refPos, filter):
    targetList = list(targets.values())

    for target in targetList:
        target.towrite = True
        if "name" in filter:
            if not filter["name"].lower() in target.name.lower():
                target.towrite = False
        if "type" in filter:
            if not filter["type"].lower() in target.objectTypes.lower():
                target.towrite = False
        if "color" in filter:
            if not filter["color"].lower() in target.color.lower():
                target.towrite = False
        if "status" in filter:
            if not filter["status"].lower() in target.objectTypes.status():
                target.towrite = False          
            
        target.setDistance(refPos)
    targetList.sort()

    i = 0
    while True :
        print(targetList[i])
        i=i+1
        if i>20:
            break

def readFile(file, targets):
    linenumber = 0
    fileStarted = False
    refLong = 0
    refLat = 0
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
                    targets[id[1:]+file].status = "dead"
                    #TODO delete tecical object
                elif id == "0":
                    pass
                    #TODO handle special object
                elif not id+file in targets:
                    newTacticalObject = tacticalObject()
                    newTacticalObject.parseLine(line, refLat, refLong, file)
                    targets[id+file] = newTacticalObject
                else:
                    targets[id+file].parseLine(line, refLat, refLong, file)
            elif "ReferenceLongitude" in line:
                refLong = int(line.split("=")[1])
            elif "ReferenceLatitude" in line:
                refLat = int(line.split("=")[1])


parser = argparse.ArgumentParser(description='Get targets')
parser.add_argument('--tacviewFile', metavar='tacviewFile', nargs='*', default=[#'H:/Tacview.txt.acmi',
                                                                                'H:/1.acmi',
                                                                                'H:/2.acmi',
                                                                                'H:/3.acmi',
                                                                                'H:/4.acmi',
                                                                                'H:/5.acmi'
                                                                                ],
                    help='unzipped tacview file')
parser.add_argument('--json', metavar='json', nargs='?', help='json')
parser.add_argument('-o', metavar='longitude', nargs='?', help='an integer for the longitude', default='55.540865')
parser.add_argument('-a', metavar='latitude', nargs='?', help='an integer for the latitude', default='26.452904')
parser.add_argument('-p', help='only arguments', action='store_true')
parser.add_argument('-n', metavar='name', nargs='?', help='name')
parser.add_argument('-t', metavar='type', nargs='?', help='filter on typ ex: antiair')
parser.add_argument('-c', metavar='type', nargs='?', help='filter on color ex: red/blue')
parser.add_argument('-s', metavar='type', nargs='?', help='filter on status dead/alive')
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
#        with open('data.json', 'w') as f:  # writing JSON object
#            json.dump(targets, f)
#            original_data = open('data.json', 'rb').read()  
#            compressed_data = zlib.compress(original_data, zlib.Z_BEST_COMPRESSION)
#            f = open('data.json.compressed', 'wb')  
#            f.write(compressed_data)  
#            f.close()
#else:
#    try:
#        json_file=open(args.json, "r")
#        targets = json.load(json_file)
#    except:
#        compressed_file=open(args.json+".compressed", "rb")
#        decompressed_data = zlib.decompress(compressed_file.read())
#        targets = json.load(decompressed_data)#TODO something is broken


longmax = latType(PosType.Lat)
longmin = 90.0
latmax = 0.0
latmin = 90.0
for target in targets.values():
    if longmax < target.geoPosition.long:
        longmax = target.geoPosition.long
#    if latmax < target["lat"]:
#        latmax = target["lat"]
#    if longmin > target["long"]:
#        longmin = target["long"]
#    if latmin > target["lat"]:
#        latmin = target["lat"]
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
    refPos = geoPosition()
    refPos.parseGeoLat(args.a)
    refPos.parseGeoLong(args.o)
    filter = {}
    if not args.n == None:
        filter["name"]=args.n
    if not args.t == None:
        filter["type"]=args.t
    if not args.c == None:
        filter["color"]=args.c
    if not args.s == None:
        filter["status"]=args.s
    print(filter)

    printTarget(targets, refPos, filter)
