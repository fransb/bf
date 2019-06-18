import argparse
from decimal import *
from pip._vendor.pytoml.writer import long
from Tools.scripts.highlight import latex_highlight

#102,T=5.738246|3.5607517|1|||359|-151467.48|-65955.93|,Type=Ground+Static+Aerodrome,Name=Oil rig,Color=Red,Coalition=Allies,Country=us

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
    tacobject["id"] = id
    tacobject["long"] = long
    tacobject["lat"] = lat
    tacobject["alt"] = alt
    tacobject["type"] = type
    tacobject["name"] = name
    tacobject["color"] = color
    tacobject["coalition"] = coalition
    tacobject["country"] = country
    tacobject["group"] = group
    
    
    return tacobject

parser = argparse.ArgumentParser(description='Get targets')
parser.add_argument('--tacviewFile', metavar='tacviewFile', nargs='?',
                    help='unzipped tacview file')

args = parser.parse_args()
if args.tacviewFile == None:
    args.tacviewFile = "H:/Tacview.txt.acmi"
targets = {}
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
            if not id in targets:
                targets[id] = parseLine(line, refLat, refLong)
                print(targets[id])
            #TODO add update of position
        elif "ReferenceLongitude" in line:
            refLong = Decimal(line.split("=")[1])
        elif "ReferenceLatitude" in line:
            refLat = Decimal(line.split("=")[1])
    
longmax = Decimal(0.0)
longmin = Decimal(90.0)
latmax = Decimal(0.0)
latmin = Decimal(90.0)
for target in targets:
    print(target)
    if longmax < target["long"]:
        longmax = target["long"]
    if latmax < target["lat"]:
        latmax = target["lat"]
    if longmin > target["long"]:
        longmin = target["long"]
    if latmin > target["lat"]:
        latmin = target["lat"]

lat = input("Enter latitude for target in format %i-%i" % (latmax, latmin))
long = input("Enter longitude for target in format xx.xxxx")
print(targets["102"])