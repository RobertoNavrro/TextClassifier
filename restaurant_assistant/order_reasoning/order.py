from enum import Enum, auto
from typing import List, Tuple, Dict
from pandas.core.series import Series
from pandas.core.frame import DataFrame
from pandas.core.reshape.merge import merge
from pandas import isna

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
    food_quality = auto()
    diet = auto()


info_keywords = {InfoType.pricerange: ['cost', 'price', 'priced', 'range'],
                 InfoType.area: ['area', 'part', 'in'],
                 InfoType.food: ['food', 'cuisine', 'serving', 'serve'],
                 InfoType.phone: ['phone', 'number'],
                 InfoType.addr: ['address', 'location', 'where'],
                 InfoType.postcode: ['postcode', 'postal', 'code'],
                 InfoType.food_quality: ['food', 'quality', 'reviews'],
                 InfoType.diet: ['diet']}


class Order:
    """
    Class to keep track of the order of the user and the possible recommendations.

    :var Dict[InfoType, str] preference: maps info type to the user preference
    :var DataFrame data: the data of all restaurants. Columns of type InfoType
    :var Dict[InfoType, List[str]] value_options: maps info type to words that occur in
        its column in the data
    :var DataFrame options: All options given the current preferences
    :var Series recommendation: the row of the restaurant that is recommended
    """

    def __init__(self):
        self.preference = {key: None for key in [InfoType.food, InfoType.pricerange, InfoType.area]}
        self.data = load_restaurant_info()
        self.data.columns = [InfoType[x] for x in self.data.columns]
        self.value_options = self.load_value_options()
        self.options = None
        self.recommendation = None
        self.extras = None

    def process_inform(self, utterance: str) -> List[Tuple[InfoType, str]]:
        """
        Processes the new request and extracts any new information. All categories that are changed
        are returned.

        :return: A list of changed values as tuples (info type, new value)
        """
        self.reset()
        changes = list()
        new_keywords = find_keywords({key: self.value_options[key] for key in self.preference},
                                     {key: info_keywords[key] for key in self.preference},
                                     utterance)
        for info_type, keyword in new_keywords:
            if self.preference[info_type] != keyword:
                changes.append((info_type, keyword))
                self.preference[info_type] = keyword

        return changes

    def process_deny(self, utterance: str) -> List[InfoType]:
        """
        Processes the input and resets all categories that are found. All categories that are
        changed are returned.

        :return: A list of changed values
        """
        self.reset()
        changes = list()
        new_keywords = find_keywords({key: self.value_options[key] for key in self.preference},
                                     {key: info_keywords[key] for key in self.preference},
                                     utterance)
        for info_type, _ in new_keywords:
            changes.append((info_type, self.preference[info_type]))
            self.preference[info_type] = None

        return changes

    def get_empty_preferences(self) -> List[InfoType]:
        """
        Get all info types for which a preference hasn't been given yet.

        :return: list of info types whose preference is unknown
        """
        empty_preferences = [info_type for info_type, preference in self.preference.items()
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
        if not self.options.empty:  # Options were already computed and there is one left
            self.recommendation = self.options.iloc[0]
            self.options = self.options[1:]

        return self.recommendation

    def set_recommendation(self, choice: int):
        self.recommendation = self.options.iloc[choice]
        self.options = self.options.drop([choice])

    def load_value_options(self) -> Dict[InfoType, List[str]]:
        """
        Puts all unique words that occur in the data that can be picked by the user,
        food, area and price range, into a dict mapping the column name to its possible values.

        :return: a dict mapping column name to its possible values
        """
        keywords = dict()
        for category in list(self.preference.keys()) + [InfoType.diet, InfoType.food_quality]:
            keywords[category] = list(set([x for x in set(self.data[category])
                                           if len(str(x)) > 0 and not isna(x)]))

        return keywords

    def reset(self) -> None:
        """
        Sets the recommendation and options to none.
        """
        self.recommendation = None
        self.options = None

    def compute_options(self) -> None:
        """
        Computes and stores all options for restaurants.
        """
        self.options = merge(DataFrame(self.preference, index=[0]), self.data)

    def __str__(self):
        return f'a restaurant serving {self.preference[InfoType.food]} food in the ' \
            f'{self.preference[InfoType.area]}, in the price range '\
            f'{self.preference[InfoType.pricerange]}'

    @staticmethod
    def str_restaurant(row: Series):
        return f'{row[InfoType.restaurantname]} serves '\
                f'{row[InfoType.food]}, is in the {row[InfoType.area]} '\
                f'and the prices are {row[InfoType.pricerange]}. Additionally, their food is '\
                f'{row[InfoType.food_quality]} and with {row[InfoType.diet]} diet options.'
