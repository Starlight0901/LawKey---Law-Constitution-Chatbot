import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

# def simplify_laws(laws):
#     simplified_laws = []
#     for law in laws:
#         # Tokenize the law text
#         tokens = nltk.word_tokenize(law)
#
#         # Simplify each word using WordNet
#         simplified_words = []
#         for token in tokens:
#             # Try finding simpler synonyms using WordNet
#             synsets = wordnet.synsets(token)
#             if synsets:
#                 # Get the first synonym (default behavior)
#                 simple_synonym = synsets[0].lemmas()[0].name()
#                 simplified_words.append(simple_synonym)
#             else:
#                 # Keep the original word if no synonym found
#                 simplified_words.append(token)
#
#         # Join simplified words back into a sentence
#         simplified_law = ' '.join(simplified_words)
#
#         simplified_laws.append(simplified_law)
#
#     return simplified_laws
