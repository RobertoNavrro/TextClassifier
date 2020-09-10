from restaurant_assistant.data_processing import data_loader
from restaurant_assistant.textclass.majority_classifier import MajorityClassifier
from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.textclass.keyword_classifier import KeywordClassifier


def main():
    train_data, test_data = data_loader.generate_dataframes(data_loader.load_dialog_data())
    classifier = MajorityClassifier()
    classifier.initialize(train_data)

    print('Welcome to the text classifier.')
    while(True):
        print('Please enter a sentence.')
        answer = input().lower()
        utterance_type = classifier.classify(answer)
        print(f'That utterance is of type {utterance_type.name}.')


if __name__ == "__main__":
    main()
