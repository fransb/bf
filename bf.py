import argparse
from decimal import *

#102,T=5.738246|3.5607517|1|||359|-151467.48|-65955.93|,Type=Ground+Static+Aerodrome,Name=Oil rig,Color=Red,Coalition=Allies,Country=us

def parseLine(line, refLat, refLong):
    tacobject = dict()
    
    for part in line.split(","):
    	if part == 
    
    tacobject["id"] = line.split(",")[0].rstrip()
    
    if 
    pos = line.split(",")[1]
    tacobject["long"] = Decimal(pos.split("|")[0].replace("T=",""))+refLong
    tacobject["lat"] = Decimal(pos.split("|")[1])+refLat
    tacobject["alt"] = pos.split("|")[2]
    typePart = line.split(",")[2:]

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
            #print(line)
            #print(line[0])
            #print(linenumber)
            fileStarted = True
            time = Decimal(line[1:])
        elif fileStarted and time == 0:
            split_line = line.split(",")
            targets[split_line[0]] = parseLine(line, refLat, refLong)
        elif "ReferenceLongitude" in line:
            refLong = Decimal(line.split("=")[1])
        elif "ReferenceLatitude" in line:
            refLat = Decimal(line.split("=")[1])
print(targets["1fe02"])