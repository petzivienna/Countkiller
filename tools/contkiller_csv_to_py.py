import csv
import os.path

outputfile = "output.py"
inputfolder = "."

directions = {"north": (0,-1),
              "east" : (1, 0),
              "south": (0, 1),
              "west" : (-1,0),
              "northeast": (1,-1),
              "southeast": (1,1),
              "southwest": (-1,1),
              "northwest": (-1,-1)
              }

output = []
connections = []

for root, dirs, files in os.walk(inputfolder):
    break # do not process subdirs
for filename in files:
    output.append(f"#======= {filename} ======")
    output.append("#------ locations -------")
    if not filename.endswith(".csv"):
        continue
    print("processing:", filename)
    with open(filename) as myfile:
        myreader = csv.reader(myfile)
        mylist = list(myreader) # nested list
    for line in mylist:
        for cell in line:
            if len(cell.strip()) > 0:
                output.append(f'Location("{cell}","{cell}")')
    #print(output)
    output.append("# ----- connections -----")
    for y, line in enumerate(mylist):
        for x, cell in enumerate(line):
            if len(cell.strip()) == 0:
                continue
            for direction in directions:
                dx, dy = directions[direction]
                if not (0 <= x+dx < len(line)):
                    continue
                if not (0 <= y+dy < len(mylist)):
                    continue
                # test if exist
                target = mylist[y+dy][x+dx]
                if len(target.strip()) == 0:
                    continue
                if (target, cell) in connections:
                    continue
                connections.append((cell, target))
                # Game.locations["hay stack"].connect("north", "farmer house")
                output.append(f'Game.locations["{cell}"].connect("{direction}", "{target}")')
    print("\n".join(output))
            
            
            
        
            
            
         


