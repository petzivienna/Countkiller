class Game:
    """containers for everything"""
    monsters = {}
    #items = {}
    locations = {}
    player = None
    current_room = None


class Location:
    
    #number = 0
    reverse = {"north":"south",
               "south":"north",
               "west":"east",
               "east":"west",
               }
    
    def __init__(self,name, description):
        #self.number = Location.number
        #Location.number += 1
        self.name = name
        Game.locations[self.name] = self
        self.description = description
        self.items = []
        self.directions = {"north":None,
                           "south":None,
                           "west":None,
                           "east":None,
                           }
        self.locked_doors = {"north":False,
                             "south":False,
                             "west":False,
                             "east":False,
                             }
                             
    def item_names(self):
        return [i.name for i in self.items]                           
        
    def connect(self,direction, location_string, one_way = False):
        if direction not in Location.reverse:
            raise ValueError(f"reverse direction unknown for: {direction}")
        self.directions[direction] = location_string
        if not one_way:
            reverse_direction = Location.reverse[direction]
        Game.locations[location_string].directions[reverse_direction] = self.name

class Monster:
    
    number = 0
    
    def __init__(self, name, description, location_string, hp=100, **kwargs):
        self.number = Monster.number
        Monster.number += 1
        Game.monsters[self.number] = self
        self.name = name
        self.description = description 
        if location_string not in Game.locations:
            raise ValueError(f"unknow location: {location_string}")
        self.location_string = location_string
        self.items = []
        self.hp = hp
        for key, value in kwargs.items():
            self.key = value
        
class Item:
    #number = 0
    
    def __init__(self, name, description, location_string=None, carrier_number=None, function=None):
        #self.number = Item.number
        #Item.number += 1
        #Game.items[self.number] = self
        if (location_string is None) and (carrier_number is None):
            raise ValueError("neither location_string nor carrier_number given")
        if (location_string is not None) and (carrier_number is not None):
            raise ValueError("loaction_string and carrier_number given. Only one is allowed")
   
        if location_string is not None:
            Game.locations[location_string].items.append(self)
        if carrier_number is not None:
            Game.monsters[carrier_number].items.append(self)
        self.name = name
        self.description = description
        self.function = function
        
    def use(self):
        if self.function is not None:
            self.function() 
        else:
            print("nothing happens")
            
            
        
def setup():
    Game.current_room = Location("hay stack","a hay stack")
    Location("farmer house", "a common house")
    Location("stables", "there are a few cows here. The evil lord replaced your horses with them")
    Location("well", "the water in here looks dirty")
    Location("barn", "your farms barn")
    Location("town road", "the road between your farm and the nearest town")
    Location("town", "a medium sized town. a lot of different people live here")
    Location("forest", "a dark and unknown forest")
   
    Game.locations["hay stack"].connect("north", "farmer house")
    Game.locations["hay stack"].connect("south", "well")
    Game.locations["hay stack"].connect("east", "barn")
    Game.locations["hay stack"].connect("west", "town road")
    Game.locations["barn"].connect("north", "stables")
    Game.locations["barn"].connect("east", "forest")
    Game.locations["farmer house"].connect("east", "stables")
    Game.locations["town road"].connect("west", "town")
    
    Game.player = Monster("Player", "You, the hero", "hay stack")
    
    Item("pitchfork","a farmers pitchfork", location_string = "hay stack")
    Item("leather jacket","a light jacket which offers a little protection", location_string = "barn")
    Item("farmers clothes", "common farmers clothes", carrier_number = 0)
    Item("bucket", "a bucket to put liquid in", location_string="farmer house", function=use_bucket)
    Item("bread", "bread", location_string="farmer house", function=eat_bread)
    

def use_bucket():
    if Game.current_room.name not in ("stables","well"):
        print("there is nothing to put in your bucket here")
        return
    if Game.current_room.name == "stables":
        print("You fill your Bucket with fresh cow milk")
        return
    if Game.current_room.name == "well":
        print("you fill your bucket with some dirty water. Some slime swims in it")
        return
        

def eat_bread():
    pass
    
   
def use_shack_key():
    """if in garde, remove key and open shack door"""
    if Game.current_room.name != "garden":
        print("not possible in this location")
        return
    Game.player.items = [i for i in Game.player.items if i.name != "shack key"]
    Game.locations["garden"].locked_doors["west"] = False
    print("You open the door to the shack. The key disappears")
    
    
def look():
    print("You are here:", Game.current_room.name)
    print("description:", Game.current_room.description)
    print("items in this room are:", [i.name for i in Game.current_room.items])
    print("directions from here:", [f"{k}:{v}" for k,v in Game.current_room.directions.items() if v is not None])
    
def inventory():
    print("you have this items:")
    for index, item in enumerate(Game.player.items):
        print(f"{index:<3} | {item.name:<20} | {item.description}")
    
def go(direction):
    # has current room a target room in this direction ?
    if Game.current_room.directions[direction] is None:
        print(f"You can not go {direction} from here")
        return
    # is the connection locked
    if Game.current_room.locked_doors[direction]:
        print(f"The door to {direction} is locked")
        return
    # go there
    Game.current_room = Game.locations[Game.current_room.directions[direction]]
    


def _take(name=None):
    """takes item with name name, offers menu if there are several of them
    returns class instance of Item"""
    if name is None:
        candidates = [i for i in Game.current_room.items]
    else:    
        candidates = [i for i in Game.current_room.items if i.name.lower() == name.lower()]

    if len(candidates) == 0:
        return None
    if len(candidates) == 1:
        return candidates[0]
    #print("candidates:", candidates)
    while True:
        # -- print list ---
        print("what do you want to pick up? press number or 0 to exit")
        ##max_name_length = max([len(i.name) for i in Game.current_room.items])
        for index, item in enumerate(candidates, 1):
            print(f"{index:<3} | {item.name} | {item.description}")
        command2 = input(">>>").strip()
        if command2 == "0":
            print("you take nothing")
            return None
        try:
            command2 = int(command2)
        except:
            print("bad input.")
            continue
        if not (0 < command2 <= len(candidates)):
            print("impossible number")
            continue
        return candidates[command2-1]
        
        
def take(command):
 
    if " " in command:
        what = " ".join(command.split()[1:]).strip()
    else:
        what = None
    obj = _take(what)
    
    if obj is None:
        if what is not None:
            print("Not possible to take", what, "from this room")
            return
        print("Nothing taken")
        return
    Game.current_room.items.remove(obj)
    Game.player.items.append(obj)
    print("You sucessfully picked up", obj.name, "and put it in your inventory")
        
def use(command):
    what = " ".join(command.split()[1:]).strip()
    if " " in command:
        what = " ".join(command.split()[1:]).strip()
    else:
        what = None
    if what is not None:            
        # is item in inventory?
        #print("itemstring:", itemstring)
        obj = [i for i in Game.player.items if i.name == what]
        if len(obj) != 1:
            print(len(obj), "of your items can be used")
            return
        obj = obj[0]
        if obj is None:
            print("You don't have such an item in your inventory")
            return
        obj.use()
    else:
        print("please specify what object you want to use")
        #todo: list of items with menu to choose 
    
def mainloop():
    look()
    while True:
        #look()
        possible_directions = [k for k,v in Game.current_room.directions.items() if v is not None]
        command = input(f"Location: {Game.current_room.name} directions: {possible_directions} >>>")
        command = command.lower().strip()
        if command in ("quit", "q", "exit"):
            break
        if command in ("north","west","south","east"):
            go(command)
        if command == "look":
            look()
        if command == "inventory":
            inventory()
        if command.startswith("use"):
            use(command)            
        if command.startswith("pickup") or command.startswith("take"):
            take(command)
            
                
            
if __name__ == "__main__":
    setup() 
    mainloop()
    print("bye")
        
