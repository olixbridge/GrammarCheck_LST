import unittest
import nltk
import bs4
import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException
from pprint import pprint
import pandas as pd
import numpy as np
import tensorflow as tf
import os
from os import listdir
from os.path import isfile, join
from collections import namedtuple
from tensorflow.python.layers.core import Dense
from tensorflow.python.ops.rnn_cell_impl import _zero_state_tensors
import time
import re
from sklearn.model_selection import train_test_split


#/Users/oliviashi/Documents/software/python/books
def load_book(path):
    input_file = os.path.join(path)
    with open(input_file) as f:
        book = f.read()
    return book

path = '/Users/oliviashi/Documents/software/python/books/4books.rtf'

# Load the books using the file names
books = []
books.append(load_book(path))


# # ## Preparing the Data
def clean_text(text):
    '''Remove unwanted characters and extra spaces from the text'''
    text = re.sub(r'\n', ' ', text) 
    text = re.sub(r'[\{}@_*>()\\#%+=\[\]]','', text)
    text = re.sub('a0','', text)
    text = re.sub('\'92t','\'t', text)
    text = re.sub('\'92s','\'s', text)
    text = re.sub('\'92m','\'m', text)
    text = re.sub('\'92ll','\'ll', text)
    text = re.sub('\'91','', text)
    text = re.sub('\'92','', text)
    text = re.sub('\'93','', text)
    text = re.sub('\'94','', text)
    text = re.sub('\.','. ', text)
    text = re.sub('\!','! ', text)
    text = re.sub('\?','? ', text)
    text = re.sub(' +',' ', text) # Removes extra spaces
    return text





# # Clean the text of the books
clean_books = []
for book in books:
    clean_books.append(clean_text(book))

# # Create a dictionary to convert the vocabulary (characters) to integers
vocab_to_int = {}
count = 0
for book in clean_books:
    for character in book:
        if character not in vocab_to_int:
            vocab_to_int[character] = count
            count += 1

# Add special tokens to vocab_to_int
codes = ['<PAD>','<EOS>','<GO>']
for code in codes:
    vocab_to_int[code] = count
    count += 1


# # Check the size of vocabulary and all of the values
# vocab_size = len(vocab_to_int)
# print("The vocabulary contains characters.".format(vocab_size))
# print(sorted(vocab_to_int))


# Create another dictionary to convert integers to their respective characters
int_to_vocab = {}
for character, value in vocab_to_int.items():
    int_to_vocab[value] = character

# Split the text from the books into sentences.
sentences = []
for book in clean_books:
    for sentence in book.split('. '):
        sentences.append(sentence + '.')



# Check to ensure the text has been split correctly.
sentences[:5]

# Convert sentences to integers
int_sentences = []

for sentence in sentences:
    int_sentence = []
    for character in sentence:
        int_sentence.append(vocab_to_int[character])
    int_sentences.append(int_sentence)

# Find the length of each sentence
lengths = []
for sentence in int_sentences:
    lengths.append(len(sentence))
lengths = pd.DataFrame(lengths, columns=["counts"])


lengths.describe()

# Limit the data we will use to train our model
max_length = 70
min_length = 10
good_sentences = []
for sentence in int_sentences:
    if len(sentence) <= max_length and len(sentence) >= min_length:
        good_sentences.append(sentence)
print("There are {} good sentences.".format(len(good_sentences)))




targeted_sentences = []
for j in range(0,len(good_sentences)):
    text = "".join([int_to_vocab[i] for i in good_sentences[j]])
    if(text.find(" has ") != -1 and text.find("'") == -1 and text.find("?") == -1):
        targeted_sentences.append(text)
    else:
        pass

print("There are {} targeted sentences.".format(len(targeted_sentences)))

# print(targeted_sentences[100])

wrong_sentences = []
for j in range(0,len(targeted_sentences)):
        wrong_sentences.append(targeted_sentences[j].replace(" has ", " have "))

print("There are {} wrong sentences.".format(len(wrong_sentences)))




configuration = ProWritingAidSDK.Configuration()
configuration.host = 'https://api.prowritingaid.com'
configuration.api_key['licenseCode'] = 'BEA9DF8B-051F-4443-A672-76B33D6873FB'
api_instance = ProWritingAidSDK.TextApi(ProWritingAidSDK.ApiClient('https://api.prowritingaid.com'))

counter = 0

for j in range (1,100):
    try: 
        wrong_sent = wrong_sentences[j]
        api_request = ProWritingAidSDK.TextAnalysisRequest(wrong_sent,
                                                ["grammar"],
                                                "General",
                                                "en")
        api_response = api_instance.post(api_request)
        tags = api_response.result.tags
        correct_sentence = wrong_sent
        for tag in reversed(tags):
                if len(tag.suggestions) != 0:
                        replacement = '' if tag.suggestions[0] == '(omit)' else tag.suggestions[0] 
                        correct_sentence = correct_sentence[0:tag.start_pos] + replacement + correct_sentence[tag.end_pos+1:]
        if correct_sentence == targeted_sentences[j]:
            counter += 1
        # print(correct_sentence)
        # print(targeted_sentences[j])
    except ApiException as e:
        print("Exception when calling TextAnalysisRequest->get: %s\n" % e)

print(counter)

