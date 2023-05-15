#from nicegui import ui, app
#from nicegui.events import ClickEventArguments
#app.add_static_files('/images',    'images' )


class Game:
    """containers for everything"""
    monsters = {}
    items = {}
    locations = {}
    player = None
    current_room = None
    game_over = False


class Location:
    
    #number = 0
    reverse = {"north":"south",
               "south":"north",
               "west":"east",
               "east":"west",
               "northeast":"southwest",
               "southwest":"northeast",
               "southeast":"northwest",
               "northwest":"southeast",
               }
    
    def __init__(self,name, description, area="village"):
        #self.number = Location.number
        #Location.number += 1
        self.name = name
        self.area = area
        Game.locations[self.name] = self
        self.description = description
        #self.items = []
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
        #self.items = []
        self.hp = hp
        self.hunger = 0
        self.thirst = 0
        for key, value in kwargs.items():
            self.key = value
        
class Item:
    number = 0
    
    def __init__(self, name, description, location_string=None, carrier_number=None, function=None, edible=False, drinkable=False):
        self.number = Item.number
        Item.number += 1
        Game.items[self.number] = self
        if (location_string is None) and (carrier_number is None):
            raise ValueError("neither location_string nor carrier_number given")
        if (location_string is not None) and (carrier_number is not None):
            raise ValueError("loaction_string and carrier_number given. Only one is allowed")
   
        #if location_string is not None:
        #    Game.locations[location_string].items.append(self)
        #if carrier_number is not None:
        #    Game.monsters[carrier_number].items.append(self)
        self.location_string = location_string
        self.carrier_number = carrier_number
        self.name = name
        self.edible = edible
        self.drinkable = drinkable
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
    Location("the stables", "there are a few cows here. The evil lord replaced your horses with them")
    Location("farm well", "the water in here looks dirty")
    Location("barn", "your farms barn")
    Location("town road", "the road between your farm and the nearest town")
    Location("iris town", "a medium sized town. a lot of different people live here")
    Location("dark forest", "a dark and unknown forest")
    Location("village blacksmith", "the local blacksmith shop. The smith is gone")
    Location("grain storage", "The evil Count has robbed this place, yet some bread is lying around")
    Location("village well", "used by everyone, which has made it dirty")
    Location("bonny stream", "a small stream with fast flowing water")
    Location("animal pens", "some sheep are here")
    Location("village fields", "your local villages fields")
    
   
    Game.locations["hay stack"].connect("north", "farmer house")
    Game.locations["hay stack"].connect("east", "barn")
    Game.locations["hay stack"].connect("south", "farm well")
    Game.locations["hay stack"].connect("west", "town road")
    
    Game.locations["farmer house"].connect("east", "the stables")
    Game.locations["farmer house"].connect("west", "village well")
    Game.locations["farmer house"].connect("north", "village fields")
    
    Game.locations["village fields"].connect("west", "village blacksmith")
    Game.locations["village fields"].connect("east", "grain storage")
    
    Game.locations["barn"].connect("north", "the stables")
    Game.locations["barn"].connect("east", "dark forest")
    Game.locations["barn"].connect("south", "bonny stream")
    
    Game.locations["farm well"].connect("east", "bonny stream")
    Game.locations["farm well"].connect("west", "animal pens")
    
    Game.locations["town road"].connect("north", "village well")
    Game.locations["town road"].connect("south", "animal pens")
    Game.locations["town road"].connect("west", "iris town")
    
    Game.locations["village well"].connect("north", "village blacksmith")
    
    Game.locations["the stables"].connect("north", "grain storage")
    
    
    Game.player = Monster("Player", "You, the hero", "hay stack")
    
    Item("pitchfork","a farmers pitchfork", location_string = "hay stack")
    Item("leather jacket","a light jacket which offers a little protection", location_string = "barn")
    Item("farmers clothes", "common farmers clothes", carrier_number = 0)
    Item("rag", "an old strip of cloth", carrier_number = 0)
    Item("rag", "an old strip of cloth", carrier_number = 0)
    Item("rag", "an old strip of cloth", carrier_number = 0)
    Item("bucket", "a bucket to put liquid in", location_string="farmer house", function=use_bucket)
    Item("bread", "bread", location_string="farmer house", function=use_bread, edible=True)
    Item("bread", "bread", location_string="farmer house", function=use_bread, edible=True)
    Item("bread", "bread", location_string="farmer house", function=use_bread, edible=True)
    Item("bread", "bread", location_string="farmer house", function=use_bread, edible=True)
    Item("bread", "bread", location_string="grain storage", function=use_bread, edible=True)
    Item("bread", "bread", location_string="grain storage", function=use_bread, edible=True)
    Item("bread", "bread", location_string="grain storage", function=use_bread, edible=True)
    Item("blacksmith hammer", "a blacksmith´s hammer", location_string="village blacksmith")
    Item("shears", "some shears, made for the keeper of the village sheep", location_string="village blacksmith", function=use_shears)
    Item("wheat", "all wheat the count has not taken or burned. Somewhat valuable", location_string="village fields")
    Item("gold coin", "the most valuable of the official coins of the kingdom", location_string="town road")
    Item("silver coin", "the second most valuable of the official coins of the kingdom", location_string="town road")
    Item("copper coin", "the least valuable of the official coins of the kingdom", location_string="town road")
    Item("copper coin", "the least valuable of the official coins of the kingdom", location_string="town road")
    Item("copper coin", "the least valuable of the official coins of the kingdom", location_string="town road")
    
def delete_item(name):
    # delete item from inventory
    for i, item in Game.items.items():
        if item.name == name and item.carrier_number == Game.player.number:
            del Game.items[i]
            return
            #break
            
def use_bucket():
    if Game.current_room.name not in ("the stables","farm well", "village well", "bonny stream"):
        print("there is nothing to put in your bucket here")
        return
    if Game.current_room.name == "the stables":
        print("You fill your Bucket with fresh cow milk")
        # delete one bucket from inventory
        delete_item("bucket")
        Item("bucket with milk", "a bucket full of fresh cow milk", carrier_number = Game.player.number,drinkable=True, function=use_bucket_with_milk)
        return
    if Game.current_room.name == "farm well":
        print("you fill your bucket with some dirty water. Some slime swims in it")
        delete_item("bucket")
        Item("bucket with dirty water", "a bucket filled to the brim with disgusting, slimy water", carrier_number = Game.player.number,drinkable=True, function=use_bucket_with_dirty_water)
        return
    if Game.current_room.name == "village well":
        print("you fill your bucket with some disgusting looking water.")
        delete_item("bucket")
        Item("bucket with dirty water", "a bucket filled to the brim with disgusting, slimy water", carrier_number = Game.player.number,drinkable=True, function=use_bucket_with_dirty_water)
        return
    if Game.current_room.name == "bonny stream":
        print("you fill your bucket with fresh water.")
        delete_item("bucket")
        Item("bucket with water", "a bucket filled to the brim with fresh water", carrier_number = Game.player.number,drinkable=True, function=use_bucket_with_water)
        return

def use_shears():
    if Game.current_room.name == "animal pens":
        print("you shear a sheep and take its fleece")
        Item("fleece", "a sheeps fleece", carrier_number = Game.player.number)
        return
        

def use_bread():
    #check for bread
    delete_item("bread")
    Game.player.hunger -= 15
    print("You eat a loaf of bread. You feel less hungry")
    Game.player.hunger = max(0, Game.player.hunger)
    return
    
def use_bucket_with_water():
    delete_item("bucket with water")
    Game.player.thirst -= 25
    print("you drink the whole bucket of water. You feel much less thirsty")
    Item("bucket", "a bucket to put liquid in", carrier_number = 0, function = use_bucket)
    Game.player.thirst = max(0, Game.player.thirst)
    return

def use_bucket_with_dirty_water():
    delete_item("bucket with dirty water")
    Game.player.thirst -= 25
    print("you drink the whole bucket of dirty water. Suddenly, you start to feel dizzy, and everything goes dark...")
    Game.player.thirst = max(0, Game.player.thirst)
    Game.game_over = True
    
def use_bucket_with_milk():
    delete_item("bucket with milk")
    Game.player.thirst -= 30
    print("you drink the whole bucket of delicious milk. You feel much less thirsty")
    Item("bucket", "a bucket to put liquid in", carrier_number = 0, function = use_bucket)
    Game.player.thirst = max(0, Game.player.thirst)
    return
    
def drop(name):
    for i, item in Game.items.items():
        if item.carrier_number == Game.player.number and item.name == name:
            item.carrier_number = None
            item.location_string = Game.current_room.name
            print("succesfully dropped:", item.name)
            return
    print("You have no such item in your inventory")
    return
    
def eat(name=None):
        # detect player items
        mystuff = [i for i, item in Game.items.items() if item.carrier_number == Game.player.number and item.name == name]
        if len(mystuff) == 0:
            print("You do not possess such an item")
            return
        myfood = [item for item in Game.items.values() if item.carrier_number == Game.player.number and item.name == name and item.edible]
        if len(myfood) == 0:
            print(f"You try to eat {name} but it is not edible")
            return
        item =myfood[0]
        item.use() # use is the same as eat
        delete_item(name)
        
def drink(name=None):
        # detect player items
        mystuff = [i for i, item in Game.items.items() if item.carrier_number == Game.player.number and item.name == name]
        if len(mystuff) == 0:
            print("You do not own something like that")
            return
        mydrink = [item for item in Game.items.values() if item.carrier_number == Game.player.number and item.name == name and item.drinkable]
        if len(mydrink) == 0:
            print(f"You try to drink {name} but it is not drinkable")
            return
        item =mydrink[0]
        item.use() # use is the same as drink
        delete_item(name)
        
  
    
def look():
    print("You are here:", Game.current_room.name)
    print("description:", Game.current_room.description)
    stuff = []
    for i, item in Game.items.items():
        if item.location_string == Game.current_room.name:
            stuff.append(item.name)
    print("items in this room:",stuff)
    print("directions from here:", [f"{k}:{v}" for k,v in Game.current_room.directions.items() if v is not None])
    # todo quantity
    
def get_description_of_item_name(item_name):
    for i, item in Game.items.items():
        if item.name == item_name:
            return item.description
    return None
        
    
def inventory():
    mystuff = [i for i, item in Game.items.items() if item.carrier_number == Game.player.number]
    if len(mystuff) == 0:
        print("you carry nothing")
        return
    
    print("you have these items:\n")
    showdict = {}
    for i, item in Game.items.items():
        if item.carrier_number == Game.player.number:
            if item.name not in showdict:
                showdict[item.name] = 1
            else:
                showdict[item.name] += 1
            
    #--- print showdict ---
    print("| name (amount)        | description")
    print("+----------------------+--------------------------")
    for item_name in showdict:
        if showdict[item_name] == 1:
            print(f"| {item_name:<20} | {get_description_of_item_name(item_name)}")
        else:
            print(f"| {item_name+' x '+str(showdict[item_name]):<20} | {get_description_of_item_name(item_name)}")
    print()
    
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
    


def take(what):
    """pick up first item with this name"""
    for i, item in Game.items.items():
        if item.name == what and item.location_string == Game.current_room.name:
            
            print("you successfully pick up:", item.name)
            item.location_string = None
            item.carrier_number = Game.player.number
            return i # item number # ????
    # item not found
    print("There is no such item here to pick up")
    return None
        
                

def use(what):
    for i, item in Game.items.items():
        if item.name == what and item.carrier_number == Game.player.number:
            item.use()
            return
    print("there is no such item in your inventory")
    return

                
        
        
    
    
def mainloop():
    look()
    while not Game.game_over:
        #look()
        possible_directions = [k for k,v in Game.current_room.directions.items() if v is not None]
        command = input(f"Location: {Game.current_room.name} directions: {possible_directions} hunger: {Game.player.hunger} thirst: {Game.player.thirst}\n >>>")
        command = command.lower().strip()
        # see pep636 - structural pattern matching https://peps.python.org/pep-0636/
        match command.split():  # creates a list
            
            case [("quit" | "q" | "exit")]:
                break
                
            case ["go", ("north" | "west" | "south" | "east") as direction] | [("north" | "west" | "south" | "east") as direction]:
                go(direction)
                Game.player.hunger += 1
                Game.player.thirst += 2
                look()
                    
            case [("look" | "inventory") as action]:      # one word only in list
                locals()[action]()   # call function with this name
            # command that need other word
            case [("eat"|"pickup"|"take"|"drop"|"drink") as action]:
                print(f"You must specify what you want to {action}")
            
            case [("pickup"|"take"), what]:
                take(what)
                look()
            
            case [("eat"|"drop"|"drink") as action, what]:
                locals()[action](what)  # call function with that name
                
            case _:
                print("i do not understand this command")
            
            
                
            
if __name__ == "__main__":
    setup() 
    mainloop()
    print("bye")
