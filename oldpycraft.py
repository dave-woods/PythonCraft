'''
Created on 23 Feb 2015

@author: David Woods
'''

import random

# Every possible item in the game
worldItems = {
    # itemName : [breakableBy, pickupable, breaksInto]
    "tree" : (["axe"], False, ["log", "log"]),
    "log" : (["axe", "punch"], True, ["twig", "twig", "twig"]),
    "twig" : ([], True, []),
    "boulder" : (["pickaxe"], False, ["rock", "rock", "rock"]),
    "rock" : ([], True, []),
    "flint" : ([], True, []),
    "sapling" : (["axe", "punch"], True, ["twig"]),
    "water" : ([], True, []),
    "sand" : ([], True, []),
    "axe" : ([], True, []),
    "pickaxe" : ([], True, []),
    "torch" : ([], True, []),
    "fire" : ([], False, []),
    "mud" : ([], True, []),
    "glass" : (["axe", "pickaxe", "punch"], False, []),
    "brick" : (["pickaxe"], True, ["rock"]),
    "plank" : (["axe"], False, ["log", "log"]),
    "door" : (["axe"], False, ["plank"]),
    "grass" : ([], True, []),
    "rope" : (["axe"], True, ["grass", "grass"])
}


naturalItems = \
{
    "tree" : 0.8,
    "log" : 0.3,
    "twig" : 0.6,
    "boulder" : 0.75,
    "rock" : 0.45,
    "flint" : 0.08,
    "sapling" : 0.94,
    "water" : 0.5,
    "sand" : 0.55,
    "mud" : 0.3,
    "grass" : 0.88
}

# Items that can be crafted from other items
craftingMenu = {
    "axe" : {"twig" : 2, "sapling" : 1},
    "pickaxe" : {"twig" : 2, "rock" : 2},
    "torch" : {"rock" : 1, "flint" : 1, "twig" : 1},
    "fire" : {"torch" : 3},
    "mud" : {"sand" : 1, "water" : 1},
    "plank" : {"log" : 2},
    "door" : {"plank" : 2},
    "tree" : {"sapling" : 1, "mud" : 1, "water": 1},
    "rope" : {"grass" : 3}
}

cookingMenu = {
    "glass" : {"sand" : 1},
    "brick" : {"mud" : 2}
}

# Items present in the world
world = {
    "room1" : {},
    "room2" : {},
    "room3" : {},
    "room4" : {},
    "room5" : {},
    "room6" : {},
    "room7" : {},
}

# Initial variable values
currentRoom = "room1"
quitEntered = False
inventory = {} #{"twig" : 2, "sapling" : 3, "rock" : 2, "torch" : 3, "sand" : 3, "water" : 2} # testing


##TODO add dinosaur
# dino spawns in a random room
# if you encounter it, he will begin chasing you
# if you stay in a room with it for two turns, it will eat you
# if you leave the room, it will follow you next turn
##TODO take a more OOP approach
# make item, actor, room objects, etc



# Function definitions
########################

# Old functions
##TODO delete

def existsHere(item):
    if item in worldItems.keys() and item in world[currentRoom].keys():
        return True
    else:
        print("That item doesn't exist here.")
        return False

def goToRoom(room):
    if room in world.keys():
        global currentRoom
        currentRoom = room
        print("You are now in " + room + "!")
    else:
        print("That room doesn't exist.")
        return False
            
def addToRoom(item, num=1):
    global world
    if item in world[currentRoom]:
        world[currentRoom][item] += num
    else:
        world[currentRoom][item] = num
        
def removeFromRoom(item, num=1):
    global world
    if item in world[currentRoom].keys():
        world[currentRoom][item] -= num
        if world[currentRoom][item] < 0:
            world[currentRoom][item] += num
            print("There's not enough to do that.")
            return False
        elif world[currentRoom][item] == 0:
            del world[currentRoom][item]
                    
def populateWorld():
    global currentRoom
    for room in world.keys():
        currentRoom = room
        for i in range(random.randrange(10, 20)):  # @UnusedVariable
            item = random.choice(list(naturalItems.keys()))
            if naturalItems[item] > random.uniform(0.01, 1.00):
                addToRoom(item, random.randrange(1, 3))

def checkInventory():
    if not inventory:
        print("You haven't found anything yet. Use the command \"pickup\" to collect items.")
    else:
        for key in sorted(inventory):
            print(key + " : " + str(inventory[key]))

def lookAtRoom():
    for key in sorted(world[currentRoom]):
        print(key + " : " + str(world[currentRoom][key]))
    roomstring = "Other rooms:"
    for key in sorted(world):
        if key != currentRoom:
            roomstring += (" " + key)
    print(roomstring)

def punch(item):
    if existsHere(item):
        print("You punched the " + item + "...")
        if "punch" in worldItems[item][0]:
            brokenInto = breakItem(item)
            print("It broke into " + str(brokenInto) + "!")
        elif item == "boulder":
            removeFromRoom(item)
            addToRoom("rock")
            print("It broke into ['rock']!")
        else:
            print("Nothing happened though.")
            return False

def swingAxe(item):
    if existsHere(item):
        print("You swung your axe at the " + item + "...")
        if "axe" in worldItems[item][0]:
            brokenInto = breakItem(item)
            print("It broke into " + str(brokenInto) + "!")
        else:
            print("Nothing happened though.")
            return False
            
def swingPickaxe(item):
    if existsHere(item):
        print("You swung your pickaxe at the " + item + "...")
        if "pickaxe" in worldItems[item][0]:
            brokenInto = breakItem(item)
            print("It broke into " + str(brokenInto) + "!")
        else:
            print("Nothing happened though.")
            return False
            
def breaksInto(item):
    global worldItems
    if item == "boulder":
        worldItems[item][2][2] = "flint" if random.randrange(4) > 0 else "rock"
    if type(worldItems[item][2]) is list:
        return worldItems[item][2]
    l = []
    l.append(worldItems[item][2])
    return l

def breakItem(item):
    removeFromRoom(item)
    brokenInto = breaksInto(item)
    for thing in brokenInto:
        addToRoom(thing)
    return brokenInto

def addToInventory(item, num=1):
    global inventory
    if item in inventory.keys():
        inventory[item] += num
    else:
        inventory[item] = num
        
def removeFromInventory(item, num=1):
    global inventory
    if item in inventory.keys():
        inventory[item] -= num
        if inventory[item] < 0:
            inventory[item] += num
            print("You don't have enough to do that.")
            return False
        elif inventory[item] == 0:
            del inventory[item]
    
def addAction(createdItem):
    global possibleActions
    global usableActions
    if createdItem in possibleActions.keys():
        usableActions[createdItem] = possibleActions[createdItem]
        del possibleActions[createdItem]
    elif createdItem == "fire":
        usableActions["cook"] = possibleActions["cook"]
        usableActions["cookfrom"] = possibleActions["cookfrom"]
        del possibleActions["cook"]
        del possibleActions["cookfrom"]
    
def pickUp(item):
    if existsHere(item):
        if worldItems[item][1]:
            world[currentRoom][item] -= 1
            if world[currentRoom][item] == 0:
                del world[currentRoom][item]
            addToInventory(item)
            print("You picked up " + ("an " if item.startswith(("a", "e", "o", "u", "i")) else "a ") + item + "!")
        else:
            print("You can't pick that up.")
            return False
                    
def place(item):
    global world
    if item in inventory.keys():
        addToRoom(item)
        removeFromInventory(item)
        print("You placed " + ("an " if item.startswith(("a", "e", "o", "u", "i")) else "a ") + item + " in " + currentRoom)
    else:
        print("You don't have that.")
        return False
                  
def isCraftFromPossible(items):
    itemDictionary = {}
    for i in items:
        if i in itemDictionary.keys():
            itemDictionary[i] += 1
        else:
            itemDictionary[i] = 1
    for key in craftingMenu:
        if craftingMenu[key] == itemDictionary:
            return key
    return False
            
def craftFromItems(items):
    if type(items) is not list:
        l = []
        l.append(items)
        del items
        items = l
    print("You tried to craft " + str(items) + "...")
    craftable = isCraftFromPossible(items)
    #print(craftable)
    if not craftable:
        print("Nothing happened.")
        return False
    else:
        craftItem(craftable)

def craftItem(item):
    if item in craftingMenu.keys():
        for ingredient in craftingMenu[item].keys():
            if ingredient not in inventory.keys() or craftingMenu[item][ingredient] > inventory[ingredient]: 
                print("Nothing happened.")
                return False
        for ingredient in craftingMenu[item].keys():
            removeFromInventory(ingredient, craftingMenu[item][ingredient])
        addToInventory(item)
        if item == "tree":
            place(item)
        print("You crafted " + ("an " if item.startswith(("a", "e", "o", "u", "i")) else "a ") + item + "!")
        print("It took " + str(craftingMenu[item]))
        print("Remember to check the command list for new options.")
        addAction(item)
        return True
    else:
        print("Nothing happened.")
        return False

def isCookFromPossible(items):
    itemDictionary = {}
    for i in items:
        if i in itemDictionary.keys():
            itemDictionary[i] += 1
        else:
            itemDictionary[i] = 1
    for key in cookingMenu:
        if cookingMenu[key] == itemDictionary:
            return key
    return False
            
def cookFromItems(items):
    if type(items) is not list:
        l = []
        l.append(items)
        del items
        items = l
    print("You tried to cook " + str(items) + "...")
    cookable = isCookFromPossible(items)
    if not cookable:
        print("Nothing happened.")
        return False
    else:
        cookItem(cookable)
            
def cookItem(item):
    if "fire" in world[currentRoom].keys():
        if item in cookingMenu.keys():
            for ingredient in cookingMenu[item].keys():
                if ingredient not in inventory.keys() or cookingMenu[item][ingredient] > inventory[ingredient]: 
                    print("Nothing happened.")
                    return False
            for ingredient in cookingMenu[item].keys():
                removeFromInventory(ingredient, cookingMenu[item][ingredient])
            addToInventory(item)
            print("You cooked " + ("an " if item.startswith(("a", "e", "o", "u", "i")) else "a ") + item + "!")
            print("It took " + str(cookingMenu[item]))
            print("Remember to check the command list for new options.")
            addAction(item)
            return True
        else:
            print("Nothing happened.")
            return False
    else:
        print("There needs to be a fire in the room to do that.")
        return False
    
def displayCommands():
    for key in sorted(usableActions):
        print(key + " " + usableActions[key][1])

def quitGame():
    global quitEntered
    quitEntered = True
        
class FalseCommandError(Exception):
    pass

########################

# Function dictionary
usableActions = {
    "punch" : (punch, "[item]\t\t\t\t- Punch an item. It might break."),
    "pickup" : (pickUp, "[item]\t\t\t\t- Try to pick up an item."),
    "place" : (place, "[item]\t\t\t\t- Place an item from your inventory in the current room."),
    "inventory" : (checkInventory, "\t\t\t\t- Look at what you've picked up."),
    "look" : (lookAtRoom, "\t\t\t\t\t- Look at what's in the room with you, and where you can go."),
    "goto" : (goToRoom, "[room]\t\t\t\t- Go to a room."),
    "?" : (displayCommands, "\t\t\t\t\t- Display this list of commands."),
    "quit" : (quitGame, "\t\t\t\t\t- Exit the game."),
    "craftfrom" : (craftFromItems, "[item (item (item (...)))]\t- Try to craft ingredients in your inventory together."),
    "craft" : (craftItem, "[item]\t\t\t\t- Try to craft an item from things in your inventory.")
}
possibleActions = {
    "axe" : (swingAxe, "[item]\t\t\t\t- Swing your axe at an item. It might break."),
    "pickaxe" : (swingPickaxe, "[item]\t\t\t\t- Swing your pickaxe at an item. It might break."),
    "cookfrom" : (cookFromItems, "[item (item (item (...)))]\t- Try to cook ingredients in your inventory over a fire."),
    "cook" : (cookItem, "[item]\t\t\t\t- Try to cook an item on the fire from things in your inventory.")
}

#################
#################
#               #
# Start Program #
#               #
#################
#################

populateWorld()
goToRoom("room1")

while not quitEntered:
    try:
        command = input("Enter an action (\"?\" for command list): ")
        commandList = command.lower().split()
        
        if len(commandList) == 0 or commandList[0] not in usableActions.keys():
            raise FalseCommandError
        else:
            action = commandList[0]
            
            if len(commandList) == 2:
                item = commandList[1]
                usableActions[action][0](item)
            elif len(commandList) > 2:
                items = commandList[1:]
                usableActions[action][0](items)
            else:
                usableActions[action][0]()
                
    except TypeError:
        print("That command didn't work properly.")
    except FalseCommandError:
        print("That command doesn't exist.")
    print()
