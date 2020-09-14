from restaurant_assistant.data_processing import data_loader
from restaurant_assistant.textclass.neural_network_classifier import NeuralNetworkClassifier


def main():
    data = data_loader.load_dialog_data()
    train_data, test_data = data_loader.generate_dataframes(data)
    classifier = NeuralNetworkClassifier()
    classifier.initialize(train_data)
    classifier.evaluate(test_data)

    print('Testing performance.')
    f1_result, acc_result = classifier.test_performance(test_data)
    print(f'F1 score: {f1_result}')
    print(f'Accuracy: {acc_result}')

    print('Welcome to the text classifier.')
    while(True):
        print('Please enter a sentence.')
        answer = input().lower()
        utterance_type = classifier.classify(answer)
        print(f'That utterance is of type {utterance_type.name}.')


if __name__ == "__main__":
    main()
