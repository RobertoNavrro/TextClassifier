from enum import Enum, auto
from typing import List, Tuple
from pandas.core.series import Series

from restaurant_assistant.data_processing.data_loader import load_restaurant_info
from restaurant_assistant.dialog.input_processor import find_keywords


class InfoType(Enum):
    restaurantname = auto()
    pricerange = auto()
    area = auto()
    food = auto()
    phone = auto()
    addr = auto()
    postcode = auto()


info_keywords = {InfoType.pricerange: ['cost', 'price', 'priced', 'range'],
                 InfoType.area: ['area', 'part', 'in'],
                 InfoType.food: ['food', 'cuisine', 'serving', 'serve'],
                 InfoType.phone: ['phone', 'number'],
                 InfoType.addr: ['address', 'location', 'where'],
                 InfoType.postcode: ['postcode', 'postal', 'code']}


class Order:

    def __init__(self):
        self.info = {key: None for key in [InfoType.food, InfoType.pricerange, InfoType.area]}
        self.data = load_restaurant_info()
        self.data.columns = [InfoType[x] for x in self.data.columns]
        self.keywords = self.load_keywords()
        self.options = self.data.copy()
        self.recommendation = None

    def process_inform(self, utterance: str) -> List[Tuple[InfoType, str]]:
        """
        Processes the new request and extracts any new information. All categories that are changed
        are returned.

        :return: A list of which values have been changed as tuples (info type, new value)
        """
        self.reset()
        changes = list()
        new_keywords = find_keywords(self.keywords,
                                     {key: info_keywords[key] for key in self.info},
                                     utterance)
        for info_type, keyword in new_keywords:
            if self.info[info_type] != keyword:
                changes.append((info_type, keyword))
                self.info[info_type] = keyword

        return changes

    def process_deny(self, utterance: str) -> List[InfoType]:
        """
        Processes the input and resets all categories that are found. All categories that are
        changed are returned.

        :return: A list of which values have been changed
        """
        self.reset()
        changes = list()
        new_keywords = find_keywords(self.keywords,
                                     {key: info_keywords[key] for key in self.info},
                                     utterance)
        for info_type, _ in new_keywords:
            changes.append((info_type, self.info[info_type]))
            self.info[info_type] = None

        return changes

    def get_empty_preferences(self):
        """
        Get all info types for which a preference hasn't been given yet.
        """
        empty_preferences = [info_type for info_type, preference in self.info.items()
                             if preference is None]
        return empty_preferences

    def get_recommendation(self) -> Series:
        """
        Returns a recommendation that hasn't been given yet, or the old recommendation if there
        are no other options.

        :return: the recommendation
        """
        if self.options is None:  # Options haven't been computed yet
            self.compute_options()
        elif not self.options.empty:  # Options were already computed and there is one left
            self.recommendation = self.options.iloc[0]
            self.options = self.options[1:]

        return self.recommendation

    def load_keywords(self):
        keywords = dict()
        for category in self.info:
            keywords[category] = [x for x in set(self.data[category]) if len(str(x)) > 0]

        return keywords

    def reset(self) -> None:
        """
        Sets the recommendation and options to none.
        """
        self.recommendation = None
        self.options = None

    def compute_options(self) -> None:
        """
        Computes and stores all options for restaurants. Sets the first option as a recommendation
        if there are options available.
        """
        self.options = self.data
        for info_type, pref in self.info.items():
            self.options = self.options[self.options[info_type] == pref].copy()

        if not self.options.empty:
            self.recommendation = self.options.iloc[0]

    def __str__(self):
        string = f'a restaurant serving {self.info[InfoType.food]} food in the ' \
            f'{self.info[InfoType.area]}, in the price range {self.info[InfoType.pricerange]}'
        return string
