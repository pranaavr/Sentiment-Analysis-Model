'''
UTILITY PROGRAM SCORER.PY
take as input the model's sentiment tagged output and compares it
with the gold standard "key" data. Reports the overall accuracy of 
the tagging and provides a confusion matrix.
'''
from sys import argv
import re

my_answer = ''

# format predictions into list
with open(argv[1], 'rb') as f:
    content = f.read()
    my_answer = content.decode("utf-16")

predictions = my_answer.replace('\r', '').split('\n')

key_text = ''
with open(argv[2], 'r') as f:
    key_text = f.read()

instances = key_text.split('<answer')
keys = []
for instance in instances:
    if "sentiment" in instance:
        s_match = re.search('sentiment="(.*)"/>', instance)
        sense = s_match.group(1)
        keys.append(sense)

print("Accuracy is: ")
key_count = 0
test_count = 0
for i in keys:
    if i == 'positive':
        key_count += 1
for i in predictions:
    if i == 'positive':
        test_count += 1

if key_count > test_count:
    print(str(test_count/key_count * 100)+'%')
elif key_count < test_count:
    print(str(key_count/test_count * 100) + '%')
