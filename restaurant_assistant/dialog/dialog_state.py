from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple
from pandas import isna

from restaurant_assistant.textclass.utterance_classifier import UtteranceType
from restaurant_assistant.order_reasoning.order import Order, InfoType, info_keywords
from restaurant_assistant.dialog.input_processor import find_keywords


pref_str = {InfoType.food: 'What kind of food would you like?',
            InfoType.area: 'Where would you like to dine?',
            InfoType.pricerange: 'What price range are you looking for?'}
repeat_str = 'I did not understand your input, could you clarify it?'


class DialogState(ABC):
    """
    A state in the dialog, which can process user inputs and return the next state and the
    response of the system. Does not retain any information of its own.
    """

    @abstractmethod
    def process_input(self, utterance: str, input_type: UtteranceType, order: Order) \
            -> Tuple[str, DialogState]:
        """
        Process the utterance and return the response and the next dialog state.
        """

    def process_inform(self, utterance: str, order: Order) -> Tuple[str, DialogState]:
        """
        Process the given inform utterance, updating the order. If all information is given,
        the state is moved to ConfirmOrder.

        :param utterance: the user input
        :param order: the current order
        :return: the system response and the next state
        """
        order.process_inform(utterance)
        empty_prefs = order.get_empty_preferences()
        if not empty_prefs:
            next_state = ConfirmOrderState()
            return_str = f'You are looking for {str(order)}. Is this correct?'
        else:
            next_state = AskPreferenceState()
            return_str = pref_str[empty_prefs[0]]

        return return_str, next_state

    def process_deny(self, utterance: str, order: Order) -> Tuple[str, DialogState]:
        """
        Process the given utterance rejecting part of the order.

        :param utterance: the user input
        :param order: the current order
        :return: the system response and the next state
        """
        next_state = AskPreferenceState()
        changes = order.process_deny(utterance)
        if not changes:
            return repeat_str

        changed_info = ', '.join([f'{info_type.name} is no longer {old_value}'
                                  for info_type, old_value in changes])
        empty = order.get_empty_preferences()
        return_str = '. '.join([changed_info, pref_str[empty[0]]])
        return return_str, next_state

    def give_new_recommendation(self, order: Order) -> Tuple[str, DialogState]:
        """
        Give a recommendation that hasn't been given before with the current query. If there
        are no new recommendations, this is communicated to the user.

        :param order: the current order
        :return: the system response and the next state
        """
        previous = order.recommendation
        recommendation = order.get_recommendation()

        if recommendation is None:
            return_str = 'I\'m afraid there is no restaurant matching your preferences. ' \
                'Please change your query.'
            next_state = AskPreferenceState()

        elif previous is not None and recommendation.equals(previous):
            return_str = 'The given recommendation is the only option.'
            next_state = RecommendationState()

        else:
            return_str = f'{recommendation[InfoType.restaurantname]} serves '\
                f'{recommendation[InfoType.food]}, is in {recommendation[InfoType.area]} '\
                f'and the prices are {recommendation[InfoType.pricerange]}.'
            next_state = RecommendationState()

        return return_str, next_state


class StartState(DialogState):
    """
    The starting state, which processes either the greeting or the first inform action of the
    user. Can either move to AskPreference or directly to ConfirmOrder if the whole order is
    given in the first input.
    """
    def process_input(self, utterance, input_type, order):
        if input_type is UtteranceType.hello:
            next_state = AskPreferenceState()
            return_str = pref_str[InfoType.food]
        elif input_type is UtteranceType.inform:
            return_str, next_state = self.process_inform(utterance, order)
        else:
            next_state = StartState()
            return_str = repeat_str

        return return_str, next_state


class AskPreferenceState(DialogState):
    """
    The state in which the user can add to or append their order. Can move to ConfirmOrder once
    the order has been completed.
    """
    def process_input(self, utterance, input_type, order):
        if input_type in [UtteranceType.inform, UtteranceType.reqalts]:
            return_str, next_state = self.process_inform(utterance, order)
        elif input_type is UtteranceType.deny:
            return_str, next_state = self.process_deny(utterance, order)
        else:
            return_str = repeat_str
            next_state = AskPreferenceState()

        return return_str, next_state


class ConfirmOrderState(DialogState):
    """
    State that checks whether the given query is correct. Can revert to AskPreference if the
    user denies parts of the order, or move to Recommendation if the recommendation is accepted.
    """

    def process_input(self, utterance, input_type, order):
        if input_type is UtteranceType.affirm:
            return_str, next_state = self.give_new_recommendation(order)

        elif input_type in [UtteranceType.negate, UtteranceType.deny]:
            return_str, next_state = self.process_deny(utterance, order)

        elif input_type is UtteranceType.reqalts:
            return_str, next_state = self.process_inform(utterance, order)

        else:
            return_str = repeat_str
            next_state = ConfirmOrderState()

        return return_str, next_state


class RecommendationState(DialogState):
    """
    State that handles queries about the given recommendation. The order cannot be changed
    anymore at this point.
    """

    def process_input(self, utterance, input_type, order):
        next_state = RecommendationState()

        if input_type is UtteranceType.reqmore:
            return_str, next_state = self.give_new_recommendation(order)
        elif input_type is UtteranceType.request:
            info = list()
            matches = find_keywords({key: info_keywords[key] for key in
                                     [InfoType.phone, InfoType.addr, InfoType.postcode]},
                                    {}, utterance)
            if not matches:
                return_str = repeat_str
            else:
                for key, _ in matches:
                    value = order.recommendation[key] \
                        if not isna(order.recommendation[key]) else 'unknown'
                    if key is InfoType.phone:
                        info.append(f'the phone number is {value}')
                    if key is InfoType.addr:
                        info.append(f'the address is {value}')
                    if key is InfoType.postcode:
                        info.append(f'the postal code is {value}')

                return_str = ', '.join(info)

        elif input_type in [UtteranceType.bye, UtteranceType.thankyou]:
            return_str = 'Thank you for using this service and see you soon!'
            next_state = None

        else:
            return_str = repeat_str

        return return_str, next_state
