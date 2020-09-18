from restaurant_assistant.data_processing import data_loader
from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.textclass.neural_network_classifier import NeuralNetworkClassifier
from restaurant_assistant.textclass.keyword_classifier import KeywordClassifier
from restaurant_assistant.dialog.dialog_state import StartState
from restaurant_assistant.order_reasoning.order import Order


def main():
    data = data_loader.load_dialog_data()
    train_data, test_data = data_loader.generate_dataframes(data)
    classifier = KeywordClassifier()
    classifier.initialize(train_data)

    print('Welcome to the restaurant assistant. You can ask for restaurants by type of food, '
          'area and price range.')
    current_state = StartState()
    order = Order()
    while(True):
        utterance = input().lower()
        input_type = classifier.classify(utterance)
        print(input_type, current_state)
        response, current_state = current_state.process_input(utterance, input_type, order)
        print(response)

        if current_state is None:
            break


if __name__ == "__main__":
    main()
