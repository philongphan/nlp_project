# from fastavro import reader
#
# with open('data.avro', 'rb') as fo:
#     avro_reader = reader(fo)
#     for record in avro_reader:
#         print(record)


# Steps:
# 1. Tokenization
# 2. Clean up irrelevant tokens
# 3.
# 3.
import json
import nltk
from nltk.corpus import stopwords
from collections import Counter

try:
    german_stopwords = stopwords.words('german')
    italian_stopwords = stopwords.words('italian')
    english_stopwords = stopwords.words('english')
except:
    nltk.download('stopwords')
    german_stopwords = stopwords.words('german')
    italian_stopwords = stopwords.words('italian')
    english_stopwords = stopwords.words('english')

# print(german_stopwords[:20])

with open("data.avro") as data:
    d = json.load(data)

try:
    tokens = nltk.word_tokenize(d['body'])
except:
    nltk.download('punkt') # for German tokenization
    tokens = nltk.word_tokenize(d['body'])

def clean_tokens(tokens, language):
    if language == 'german':
        stopwords = german_stopwords
    elif language == 'italian':
        stopwords = italian_stopwords
    elif language == 'english':
        stopwords = english_stopwords

    tokens = [token.lower() for token in tokens]
    tokens = Counter(tokens)
    punctuations = ['.', ',', ':', '?', '!', '(', ')', '-', '–', '*', '"', '„', '“']
    tokens = {i:tokens[i] for i in tokens if (i not in stopwords) and (i not in punctuations)}
    return tokens

tokens = clean_tokens(tokens, language='german')

query = {
    'first': 'markus',
    'last': 'söder',
    'company': 'Adidas AG'

}

def find_match(query: dict, text):
    try:
        first_freq = text[query['first']]
    except:
        first_freq = 0

    try:
        last_freq = text[query['last']]
    except:
        last_freq = 0

    return {
        query['first']: first_freq,
        query['last']: last_freq
    }


print(find_match(query, tokens))

# Fuzzy matching
# Regex

# How to find company names?
# e.g. Schwarzkopf GmbH
# If we have names with multiple words, they should all come up in the text

print(query['last'] in d['body'].lower())
print(query['first'] in d['body'].lower())
print(f"{query['first']} {query['last']}" in d['body'].lower())


# How to treat double names
# e.g. Meier-Umlauf