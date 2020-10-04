from _io import BytesIO
import argparse
from gtts import gTTS
import contextlib

from restaurant_assistant.data_processing import data_loader
from restaurant_assistant.dialog.dialog_state import StartState
from restaurant_assistant.order_reasoning.order import Order
from restaurant_assistant.textclass.neural_network_classifier import NeuralNetworkClassifier
from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.textclass.keyword_classifier import KeywordClassifier
from restaurant_assistant.textclass.majority_classifier import MajorityClassifier
from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier, UtteranceType

with contextlib.redirect_stdout(None):
    import pygame


def output(text: str, speech: bool, uppercase: bool) -> None:
    """
    Prints the given text and converts it to spoken output if speech is true.

    :param text: the text that needs to be communicated to the user
    :param speech: whether the text should be converted to audio
    :param uppercase: whether the text should be printed in all-caps
    """
    conv_text = text.upper() if uppercase else text
    print(conv_text)

    if speech:
        tts = gTTS(text=text, lang='en', slow=False)
        mp3 = BytesIO()
        tts.write_to_fp(mp3)
        mp3.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(mp3)
        pygame.mixer.music.play()


def run_assistant(classifier: UtteranceClassifier, test: bool, speech: bool,
                  nr_recs: int, restart: bool, uppercase: bool) -> None:
    """
    Runs the restaurant assistant with the given parameters.

    :param classifier: the classifier to use for text classification
    :param test: whether to test the classifier
    :param speech: whether to convert the program output to audio
    :param nr_recs: the maximum amount of recommendations that the system can give
    :param restart: whether program restarts are allowed
    :param uppercase: whether to convert the program output to uppercase
    """
    data = data_loader.load_dialog_data()
    train_data, test_data = data_loader.generate_dataframes(data)
    classifier.initialize(train_data)
    if test:
        output('Testing the classifier..', speech, uppercase)
        f1_score, accuracy = classifier.test_performance(test_data)
        result = f'F1 score: {round(f1_score, 2)}\nAccuracy: {round(accuracy, 3)}'
        output(result, speech, uppercase)

    output('Welcome to the restaurant assistant. You can ask for restaurants by type of food, '
           'area and price range.', speech, uppercase)
    current_state = StartState()
    order = Order(nr_recs)
    while(True):
        utterance = input().lower()
        input_type = classifier.classify(utterance)

        if restart and input_type is UtteranceType.restart:
            order = Order(nr_recs)
            current_state = StartState()
            output('Your order has been cleared. Please state your new order.', speech, uppercase)
            continue

        response, current_state = current_state.process_input(utterance, input_type, order)
        output(response, speech, uppercase)

        if current_state is None:
            break


def main():
    """
    Get the arguments given by the user.
    """
    parser = argparse.ArgumentParser(description='Start the restaurant assistant')

    parser.add_argument('-c --classifier', type=str, default='decision_tree',
                        choices=['neural_network', 'decision_tree', 'keyword', 'majority'],
                        dest='classifier', help='Choose which classifier to use to '
                        'classify the user input. Default is decision_tree.')

    parser.add_argument('-t --test', action='store_true', dest='test',
                        help='Test the performance of the classifier.')

    parser.add_argument('-s --speech', action='store_true', dest='speech',
                        help='Read all output out loud')

    parser.add_argument('-n --nr_recs', type=int, default=3, dest='nr_recs',
                        help='Decide the maximum amount of recommendations that '
                        'are given at a time. The default is 3.')

    parser.add_argument('-r --restart', action='store_true', dest='restart',
                        help='Allow for restarts of the program.')

    parser.add_argument('-u --uppercase', action='store_true', dest='uppercase',
                        help='Prints all system output in uppercase letters.')

    args = parser.parse_args()

    if args.classifier == 'neural_network':
        classifier = NeuralNetworkClassifier()
    elif args.classifier == 'decision_tree':
        classifier = DecisionTreeClassifier()
    elif args.classifier == 'keyword':
        classifier = KeywordClassifier()
    elif args.classifier == 'majority':
        classifier = MajorityClassifier()
    else:
        raise Exception(f'The given classifier, {args.classifier}, is unknown.')

    run_assistant(classifier, args.test, args.speech, args.nr_recs, args.restart, args.uppercase)


if __name__ == "__main__":
    main()
