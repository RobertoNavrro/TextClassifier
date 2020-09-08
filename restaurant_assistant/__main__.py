from restaurant_assistant.data_processing import data_loader
from restaurant_assistant.textclass.majority_classifier import MajorityClassifier
from restaurant_assistant.textclass.keyword_classifier import KeywordClassifier

def main():
    df = data_loader.generate_dataframe(data_loader.load_dialog_data())
    classifier = KeywordClassifier()
    classifier.initialize(df)

    print('Welcome to the text classifier.')
    while(True):
        print('Please enter a sentence.')
        answer = input().lower()
        print(answer)
        utterance_type = classifier.classify(answer)
        print(f'That utterance is of type {utterance_type.name}.')

if __name__ == "__main__":
    main()
