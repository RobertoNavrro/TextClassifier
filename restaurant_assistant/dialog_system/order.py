from enum import Enum, auto
from restaurant_assistant.data_processing import data_loader

class EntryType(Enum):
    """
    Enumeration containing all possible types of utterances.
    """
    food = auto()
    price = auto()
    area = auto()

class UserOrder():
    def __init__(self):
        self.preferences = {'food' :None,'price' : None, 'area': None}
        self.database = data_loader.load_restaurant_dataset()
        self.recommendation = list()
        
    def stackFull(self):
        for value in self.preferences.values():
            print(f"Here is the val:{value}")
            if value is None:
                return False
        return True
    
    def findMissingType(self):
        if self.preferences.get('food') is None:
            print("What type of food are you looking for?")
            return
        if self.preferences.get('price') is None:
            print("Do you want a cheap, moderate or expensive restaurant?")
            return
        if self.preferences.get('area') is None:
            print("Where in the city would you want it to be?")
            return
        pass
    
    def displayOrder(self):
        print(f"You requested {self.preferences.get('food')} food, at a {self.preferences.get('price')} priced restaurant, in {self.preferences.get('area')}.")
    
    def displaySuggestion(self):
        
        pass
    
    def processOrder(self, user_pref):
        for preference in user_pref:
            if preference[0] is EntryType.food:
                self.preferences.update('food',preference[1])
            if preference[0] is EntryType.price:
                 self.preferences.update('price',preference[1])
            if preference[0] is EntryType.area:
                 self.preferences.update('area',preference[1])
    
    
        
        