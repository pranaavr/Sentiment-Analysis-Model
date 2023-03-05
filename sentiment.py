'''
Programming Assignment 5
Pranaav Rao
Uses bag of words model to determine sentiment of test
data.
'''
import math
from sys import argv
import re
from nltk.corpus import stopwords
import json

#used later for preprocessing
def num_there(s):
    return any(i.isdigit() for i in s)

train = ''
test = ''

#for preprocessing
punc = '''.,-?!:;_[]{}()'"|\&$%'''

#open line-train into string
with open(argv[1], 'r') as f:
    train += f.read()

with open(argv[2], 'r') as f:
    test += f.read()

#split by instance
train_instances = train.replace('\n','').split('</instance>')

#map each context word to the associated sense while recording frequency
neg_sense = {}
pos_sense = {}
for instance in train_instances:
    if "id=" in instance:
        c_match = re.search('<context>(.*)</context>', instance)
        context = c_match.group(1)
        #pre-processing
        # 1. remove punctuation
        # 2. remove special characters
        # 3. remove numerics
        # 4. remove stop words
        context = context.lower()
        for ptr in context:
            if ptr in punc:
                context = context.replace(ptr, "")
        sentenceWords = context.split()
        for i in sentenceWords[:]:
                if num_there(i) or i in set(stopwords.words('english')):
                    sentenceWords.remove(i)
        if 'sentiment="negative"' in instance:
            for i in sentenceWords:
                if i in neg_sense:
                    neg_sense[i] += 1
                else:
                    neg_sense[i] = 1
        elif 'sentiment="positive"' in instance:
            for i in sentenceWords:
                if i in pos_sense:
                    pos_sense[i] += 1
                else:
                    pos_sense[i] = 1

# dictionary that records frequency of positive and negative for each word
# bag of words model
word_sense = {}
for i in neg_sense:
    word_sense[i] = {'negative':neg_sense[i]}
for i in pos_sense:
    word_sense[i] = {'positive':pos_sense[i]}
for i in word_sense:
    # 0.001 to work with the log-likelihood formula
    if 'positive' not in word_sense[i].keys():
        word_sense[i]['positive'] = 0.001
    elif 'negative' not in word_sense[i].keys():
        word_sense[i]['negative'] = 0.001
    #log-likelihood
    word_sense[i]['likelihood'] = abs(math.log(word_sense[i]['positive']/word_sense[i]['negative']))
    #sense
    if word_sense[i]['positive'] > word_sense[i]['negative']:
        word_sense[i]['sentiment'] = 'positive'
    else:
        word_sense[i]['sentiment'] = 'negative'

with open(argv[3], 'w') as f:
    f.write('DECISION LIST MODEL:\n')
    f.write(json.dumps(word_sense))       


#retrieve instances from test
test_instances = test.replace('\n','').split('</instance>')
#retrieve sentences for each id
test_sentences = []
for instance in test_instances:
    if "id=" in instance:
        c_match = re.search('<context>(.*)</context>', instance)
        sentence = c_match.group(1)
        #pre process
        sentence.lower()
        for ptr in sentence:
            if ptr in punc:
                sentence = sentence.replace(ptr, "")
        sentenceWords = sentence.split()
        for i in sentenceWords[:]:
                if num_there(i) or i in set(stopwords.words('english')):
                    sentenceWords.remove(i)
        sentence = ' '.join(sentenceWords)
        test_sentences.append(sentence)

#make predictions on test sentence
for i in test_sentences:
    count = 0
    i_words = i.split()
    for word in i_words:
        if word in word_sense:
            if word_sense[word]['sentiment'] == 'positive':
                count += 1
            elif word_sense[word]['sentiment'] == 'negative':
                count -= 1
    if count > 0:
        print('positive')
    elif count <= 0:
        print('negative')
