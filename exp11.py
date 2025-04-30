import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Download necessary data for tokenization (only needed once)
nltk.download('punkt')

# Take input from the user
text = input("Enter your text: ")

# Sentence Tokenization
sentences = sent_tokenize(text)
print("\nSentence Tokenization:")
print(sentences)

# Word Tokenization
words = word_tokenize(text)
print("\nWord Tokenization:")
print(words)
