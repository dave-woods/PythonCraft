'''
Created on 27 Feb 2015

@author: David
'''
class Item(object):
    def __init__(self, itemType, destroyedBy=[], destroyedTo=[], storable=False):
        self.itemType = itemType
        self.destroyedBy = destroyedBy
        self.destroyedTo = destroyedTo
        self.storable = storable
    
    def isDestroyedBy(self, item):
        return item in self.destroyedBy
    
    def getFragments(self):
        return self.destroyedTo
    
    def isStorable(self):
        return self.storable
    
    def __str__(self):
        return self.itemType
    
class NaturalItem(Item):
    def __init__(self, itemType, spawnChance, destroyedBy=[], destroyedTo=[], storable=False):
        Item.__init__(self, itemType, destroyedBy, destroyedTo, storable)
        self.spawnChance = spawnChance
        
class GrowingItem(NaturalItem):
    def __init__(self, itemType, spawnChance, recipe, destroyedBy=[], destroyedTo=[], storable=False):
        NaturalItem.__init__(self, itemType, spawnChance, destroyedBy=[], destroyedTo=[], storable=False)
        self.recipe = recipe
        
class CraftableItem(Item):
    def __init__(self, itemType, recipe, destroyedBy=[], destroyedTo=[], storable=False):
        Item.__init__(self, itemType, destroyedBy, destroyedTo, storable)
        self.recipe = recipe
        
class CookableItem(Item):
    def __init__(self, itemType, recipe, destroyedBy=[], destroyedTo=[], storable=False):
        Item.__init__(self, itemType, destroyedBy, destroyedTo, storable)
        self.recipe = recipe