import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


nltk.download('punkt')
nltk.download('stopwords')


def law_cleaning(law):
    # Remove punctuations
    law = law.translate(str.maketrans('', '', string.punctuation + '\r\n\t'))

    # Remove special characters
    law = law.replace('ã', '')
    law = law.replace('Ã', '')

    # Remain only the alphabetic, numeric characters and whitespaces
    law = ''.join([i for i in law if i.isalnum() or i.isspace()])
    return law


def tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    return tokens


def remove_stopwords(tokens):
    stop_words = set(stopwords.words("english"))
    filtered = [token for token in tokens if token.lower() not in stop_words]
    return filtered


def stemmer(tokens):
    # Create the Porter stemmer object
    pstemmer = PorterStemmer()
    stemmed_words = [pstemmer.stem(token) for token in tokens]
    # Join the list of stemmed words into a single string separated by spaces
    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text