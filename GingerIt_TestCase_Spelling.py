import unittest
from gingerit.gingerit import GingerIt
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

#/Users/oliviashi/Documents/software/python/books
def load_book(path):
    input_file = os.path.join(path)
    with open(input_file) as f:
        book = f.read()
    return book

# Collect all of the book file names
path = '/Users/oliviashi/Documents/software/python/books/Alices_Adventures_in_Wonderland_by_Lewis_Carroll.rtf'

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
max_length = 150
min_length = 10
good_sentences = []
for sentence in int_sentences:
    if len(sentence) <= max_length and len(sentence) >= min_length:
        good_sentences.append(sentence)


print("There are {} good sentences.".format(len(good_sentences)))


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
           'n','o','p','q','r','s','t','u','v','w','x','y','z',]
def noise_maker(sentence, threshold):
    
    noisy_sentence = []
    i = 0
    while i < len(sentence):
        random = np.random.uniform(0,1,1)
        if random < threshold:
            noisy_sentence.append(sentence[i])
        else:
            new_random = np.random.uniform(0,1,1)
            if new_random > 0.67:
                if i == (len(sentence) - 1):
                    continue
                else:
                    noisy_sentence.append(sentence[i+1])
                    noisy_sentence.append(sentence[i])
                    i += 1
            elif new_random < 0.33:
                random_letter = np.random.choice(letters, 1)[0]
                noisy_sentence.append(vocab_to_int[random_letter])
                noisy_sentence.append(sentence[i])
            else:
                pass     
        i += 1
    return noisy_sentence


# print("".join([int_to_vocab[i] for i in noise_maker(good_sentences[0], 0.99)]) )




class TestGingerIt(unittest.TestCase):
    def test(self):
        j = 0
        text = "".join([int_to_vocab[i] for i in noise_maker(good_sentences[j], 0.99)]) + " "
        parser = GingerIt()
        output = parser.parse(text)
        self.assertEqual(
            output.get("result"), "".join([int_to_vocab[i] for i in good_sentences[j]])
        )

if __name__ == '__main__':
    unittest.main()