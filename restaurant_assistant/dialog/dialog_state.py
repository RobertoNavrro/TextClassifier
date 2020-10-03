from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple
from pandas import isna

from restaurant_assistant.textclass.utterance_classifier import UtteranceType
from restaurant_assistant.order_reasoning.order import Order, InfoType, info_keywords
from restaurant_assistant.dialog.input_processor import find_keywords
from restaurant_assistant.order_reasoning.order_reasoner import process_extra


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
        order.compute_options()
        option_count = order.options.shape[0]
        if option_count >= 2:
            if not empty_prefs:
                next_state = ConfirmOrderState()
                return_str = f'You are looking for {str(order)}. Is this correct?'
            else:
                next_state = AskPreferenceState()
                return_str = pref_str[empty_prefs[0]]
        elif option_count == 1:
            next_state = ConfirmOrderState()
            return_str = f'You are looking for {str(order)}. Is this correct?'
        elif option_count == 0:
            next_state = OrderConflictState()
            return_str = f'There are no matches for {str(order)}. Would you like to '\
                'see alternatives?'

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
            return_str = "Please state the property that you want to change, like 'no Italian'."
        else:
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
            return_str = Order.str_restaurant(order.recommendation) + \
                ' Do you want this restaurant?'
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
            order.compute_options()
            return_str = 'Do you have any additional requirements? Please state them if applicable.'
            next_state = AdditionalRequirementState()

        elif input_type in [UtteranceType.negate, UtteranceType.deny]:
            return_str, next_state = self.process_deny(utterance, order)

        elif input_type is UtteranceType.reqalts:
            return_str, next_state = self.process_inform(utterance, order)

        else:
            return_str = repeat_str
            next_state = ConfirmOrderState()

        return return_str, next_state


class AdditionalRequirementState(DialogState):
    """
    Processes any additional requirements if given, moving to GetChoiceState.
    If not, a random recommendation is given, and move to either AskPreference or Recommendation
    based on whether there's an option.
    """
    def process_input(self, utterance, input_type, order):
        if input_type is UtteranceType.negate:
            return_str, next_state = self.give_new_recommendation(order)
        else:
            rest_strs = process_extra(utterance, order.options, order.value_options)
            return_str = 'The following options are available, please choose by number:\n\n'
            return_str = return_str + '\n'.join(rest_strs)
            next_state = GetChoiceState()

        return return_str, next_state


class OrderConflictState(DialogState):
    """
    The state in which we identify no restaurant matches the user's desire. If we obtain an
    affirmation, we display possible alternatives, otherwise we request the user to
    change preferences.
    """
    def process_input(self, utterance, input_type, order):
        if input_type is UtteranceType.affirm or input_type is UtteranceType.reqalts:
            return_str = order.compute_alternatives()
            if return_str is None:
                order.reset()
                order.reset_preferences()
                next_state = AskPreferenceState()
                return_str = 'We are sorry to inform you there are no alternatives. Please indicate new preferences.'
            else:
                next_state = GetChoiceState()
        elif input_type is UtteranceType.negate:
            order.reset()
            order.reset_preferences()
            empty_prefs = order.get_empty_preferences()
            return_str = pref_str[empty_prefs[0]]
            next_state = AskPreferenceState()
        else:
            return_str = repeat_str
            next_state = OrderConflictState()

        return return_str, next_state


class GetChoiceState(DialogState):
    """
    State in which the restaurant choice of the user is processed. If processed correctly,
    the next state is InformChoice.
    """
    def process_input(self, utterance, input_type, order):
        try:
            choice = int(utterance)
            order.set_recommendation(choice)
            return_str = f'You have chosen {order.recommendation[InfoType.restaurantname]}. ' \
                'You can ask for their phone number, address and postal code.'
            next_state = InformChoiceState()

        except Exception:
            return_str = repeat_str
            next_state = GetChoiceState()

        return return_str, next_state


class RecommendationState(DialogState):
    """
    State that gives a recommendation out of the possible options. The order cannot be changed
    anymore at this point. Can move to InformChoice if the restaurant is accepted.
    """
    def process_input(self, utterance, input_type, order):
        if input_type in [UtteranceType.reqmore, UtteranceType.negate]:
            return_str, next_state = self.give_new_recommendation(order)

        elif input_type is UtteranceType.affirm:
            return_str = f'You have chosen {order.recommendation[InfoType.restaurantname]}. ' \
                'You can ask for their phone number, address and postal code.'
            next_state = InformChoiceState()

        else:
            return_str = repeat_str
            next_state = RecommendationState()

        return return_str, next_state


class InformChoiceState(DialogState):
    """
    State that answers questions about the chosen restaurant.
    """

    def process_input(self, utterance, input_type, order):
        next_state = InformChoiceState()
        if input_type is UtteranceType.request:
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
                        info.append(f'the phone number is {value}.')
                    if key is InfoType.addr:
                        info.append(f'the address is {value}.')
                    if key is InfoType.postcode:
                        info.append(f'the postal code is {value}.')

                return_str = ', '.join(info)

        elif input_type in [UtteranceType.bye, UtteranceType.thankyou]:
            return_str = 'Thank you for using this service and see you soon!'
            next_state = None

        else:
            return_str = repeat_str

        return return_str, next_state
