from typing import Dict, Tuple, List, Union
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from pandas import isna

from restaurant_assistant.dialog.input_processor import find_keywords
from restaurant_assistant.order_reasoning.order import Order, InfoType, info_keywords

extras = ['romantic', 'children', 'long time', 'busy', 'big portions', 'healthy']


class Rule():
    """
    A rule that can be applied to the database to infer properties.

    :var int id: the identifier of the rule
    :var Dict[Union[InfoType, str], Union[str, bool]] antecedent: the requirements that should hold
        for the rule to apply
    :var Union[str, InfoType] consequent: the value that is assigned based on the antecedent
    :var bool value: the assigned value of the consequent
    """
    def __init__(self, index: int,
                 antecedent: Dict[Union[InfoType, str], Union[str, bool]],
                 consequent: str, value: bool):
        self.id = index
        self.antecedent = antecedent
        self.consequent = consequent
        self.value = value

    def apply(self, data: Series, requests: List[Tuple[str, bool]]) \
            -> Tuple[bool, Tuple[str, bool]]:
        """
        Applies the rule to the given row. Returns whether values were changed and whether it's
        relevant for the request

        :var data: the row with information about a single restaurant
        :var requests: list of properties and their values which are requested

        :return: whether the row should be changed and whether the consequent matches one of the
            requests as a tuple (property, bool same value)
        """
        new_value = False
        relevant = None
        match = False

        if all(data[key] == value for key, value in self.antecedent.items()):
            match = True
            new_value = isna(data[self.consequent])

        if match:
            for request, value in requests:
                if request == self.consequent:
                    relevant = (request, self.value == value)

        return new_value, relevant

    def __str__(self):
        str_antecedent = {x.name if isinstance(x, InfoType) else x: value
                          for x, value in self.antecedent.items()}
        return f'Rule {self.id}: {str_antecedent} -> {self.consequent}: {self.value}'


def get_rules() -> List[Rule]:
    """
    Helper function to load all rules.

    :return: all rules.
    """
    rule1 = Rule(1, {InfoType.pricerange: 'cheap', InfoType.food_quality: 'good'}, 'busy', True)
    rule2 = Rule(2, {InfoType.food: 'spanish'}, 'long time', True)
    rule3 = Rule(3, {'busy': True}, 'long time', True)
    rule4 = Rule(4, {'long time': True}, 'children', False)
    rule5 = Rule(5, {'busy': True}, 'romantic', False)
    rule6 = Rule(6, {'long time': True}, 'romantic', True)
    rule7 = Rule(7, {InfoType.food: 'french'}, 'big portions', False)
    rule16 = Rule(16, {InfoType.food: 'chinese'}, 'big portions', True)
    rule14 = Rule(14, {InfoType.food_quality: 'good', InfoType.pricerange: 'moderate'},
                  'big portions', True)
    rule8 = Rule(8, {InfoType.diet: 'meat', InfoType.pricerange: 'cheap'}, 'big portions', True)
    rule9 = Rule(9, {InfoType.area: 'centre', InfoType.diet: 'vegan'}, 'busy', True)
    rule10 = Rule(10, {'big portions': True, InfoType.diet: 'meat'}, 'healthy', False)
    rule11 = Rule(11, {InfoType.diet: 'vegetarian'}, 'healthy', True)
    rule12 = Rule(12, {'healthy': True}, 'children', True)
    rule13 = Rule(13, {'big portions': True, 'children': True}, 'long time', True)
    rule15 = Rule(15, {InfoType.diet: 'vegan', 'big portions': True}, 'healthy', True)

    return [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12,
            rule13, rule14, rule15, rule16]


def process_extra(utterance: str, options: DataFrame, value_options: Dict[InfoType, List[str]]) \
        -> List[str]:
    """
    Extracts all additional preferences. Applies the implication rules to all restaurants, and
    returns strings for each restaurant that contain the applied rules and whether they are
    recommended.

    :return: list of strings with one string for each restaurant, denoting the applied rules
        and  whether they are recommended.
    """
    extras_values = {key: value for key, value in value_options.items()
                     if key in [InfoType.food_quality, InfoType.diet]}
    help_values = {key: value for key, value in info_keywords.items()
                   if key in [InfoType.food_quality, InfoType.diet]}

    column_values = find_keywords(extras_values, help_values, utterance)

    other_values = [(x, True) for x in extras if x in utterance]
    column_values.extend(other_values)

    for extra in extras:
        options[extra] = Series(dtype='bool')

    rules = get_rules()
    return_strs = list()

    for i in options.index:
        rest_str = f'{i}: {Order.str_restaurant(options.loc[i])}\n'
        for key, value in column_values:
            if key in options.columns and options.at[i, key] == value:
                rest_str = rest_str + f'{options.at[i, InfoType.restaurantname]} is ' \
                        f'recommended, based on preference {key.name}: {value}.\n'
                break
        else:
            loop = True
            stack = list()
            while(loop):
                loop = False
                for rule in rules:
                    new_value, relevant_request = rule.apply(options.loc[i], column_values)
                    if relevant_request:
                        stack.append(rule)
                        for rule in stack:
                            rest_str = rest_str + f'{str(rule)}\n'

                        rec = '' if relevant_request[1] else 'not '
                        rest_str = rest_str + f'{options.at[i, InfoType.restaurantname]} is {rec}' \
                            f'recommended, based on preference {relevant_request[0]}.\n'

                        loop = False
                        break

                    if new_value:
                        options.at[i, rule.consequent] = rule.value
                        stack.append(rule)
                        loop = True

        return_strs.append(rest_str)

    return return_strs