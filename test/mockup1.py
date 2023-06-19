import PySimpleGUI as sg

class Game:
    rooms = {}
    items = {}
    room = None

class Room:
    def __init__(self, name, imagename, connections,
                 description="blabla"):
        self.name = name
        self.imagename = imagename
        self.description = description
        self.connections = connections # {"north":"forest", ...}
        Game.rooms[name] = self

Room("village", "village.png", {"south":"port"})
Room("port", "port_city.png", {"north":"village"}, "bla\nblabla\nblablabla!")

Game.room = Game.rooms["village"]
# ----------

layout = [
    [sg.Text("you are in this location:"), 
     sg.Text("village", key="location_name", size=(30,1))],
    [sg.Image(filename="village.png", key="location_image")],
    [sg.Text("bla bla bla\n bla bla bla", key="location_description",
             size=(30,5))],
    [sg.Text("possible directions:"), 
     sg.Text("{'south':'port'}", key="location_directions" )],
    [sg.Multiline(default_text = "You wake up in a village.",
                  disabled=True, autoscroll=True,
                  size=(40,10), key="output")],
    [sg.InputText(size=(30,1), key="command",focus=True), 
     sg.Button("OK", bind_return_key=True)],
    [sg.Button("Quit")],
]

window = sg.Window("mockup", layout=layout,
                   return_keyboard_events=True)
#window.finalize()

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Quit"):
        break
    if event == "OK":
        print(event, values)
        if values["command"] in Game.room.connections:
            # change room
            new_room_name = Game.room.connections[values["command"]]
            Game.room = Game.rooms[new_room_name]
            window["output"].update(f"You go to {new_room_name}")
            window["location_name"].update(new_room_name)
            window["location_image"].update(filename=Game.room.imagename)
            window["location_description"].update(Game.room.description)
            window["command"].update("")

window.close()

