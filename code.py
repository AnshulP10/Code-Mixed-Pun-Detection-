import re
import enchant
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate 
from nltk.corpus import brown, reuters, gutenberg
from nltk import bigrams, trigrams
from collections import Counter, defaultdict  
from nltk.corpus import words
word_list = words.words()     

def hindi_transliterate(data):
    text = transliterate(data,sanscript.ITRANS,sanscript.DEVANAGARI)
    return text


def strtokenize(string):
    string = re.sub('[,.?!;:"]','',string)
    arr = string.split()
    return arr

def train():

    for sentence in reuters.sents():
        for w1, w2 in bigrams(sentence, pad_right=True, pad_left=True):
            model[w1][w2] += 1
    for sentence in brown.sents():
        for w1, w2 in bigrams(sentence, pad_right=True, pad_left=True):
            model[w1][w2] += 1     
    for sentence in brown.sents():
        for w1, w2 in bigrams(sentence, pad_right=True, pad_left=True):
            model[w1][w2] += 1    
    for w1 in model:        
        total_count = float(sum(model[w1].values()))
        for w2 in model[w1]:
            model[w1][w2] /= total_count
def get_levenshtein_distance(word1, word2):

    word2 = word2.lower()
    word1 = word1.lower()
    matrix = [[0 for x in range(len(word2) + 1)] for x in range(len(word1) + 1)]

    for x in range(len(word1) + 1):
        matrix[x][0] = x
    for y in range(len(word2) + 1):
        matrix[0][y] = y

    for x in range(1, len(word1) + 1):
        for y in range(1, len(word2) + 1):
            if word1[x - 1] == word2[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1,
                    matrix[x][y - 1] + 1
                )

    return matrix[len(word1)][len(word2)]


def soundex(query: str):

    query = query.lower()
    letters = [char for char in query if char.isalpha()]


    if len(query) == 1:
        return query + "000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = letters[0]
    letters = letters[1:]
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"


    to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    first_letter = [value if first_letter else first_letter for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]

    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]

    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])

    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    return string


model = defaultdict(lambda: defaultdict(lambda: 0))
train()
zz =str(input("Enter String : "))
file1 = open('hinData.txt', 'r')
hindata = file1.read()
arr1 = strtokenize(hindata)
unique = set(arr1)
dic = list(unique)

arr = strtokenize(zz)
d = enchant.Dict("en_US")
en = []
hin = []
non_en = []
lent = -1
index = 0
cand=[]
for i in arr :
    lent+=1
    if d.check(i):
        en.append(i)
        word = hindi_transliterate(i)
        if word in dic:
            print(word)
            cand.append(lent)
            hin.append(arr[lent])
    else:
        word = hindi_transliterate(i)
        print(word)
        if word in dic:
            cand.append(lent)
            hin.append(arr[lent])
        else:
            cand.append(lent)
            hin.append(arr[lent])
print(f"English Words : {en}")
print(f"Hindi Words : {hin}")

print(f"candidate words : {cand}")

for ind in cand:
    print(f"candidate word = {arr[ind]}")
    for word3 in word_list:
        string1 = arr[ind];
        string2 = word3
        ans1=soundex(string1)
        ans2=soundex(string2)
        if ans1[1:]==ans2[1:]:
            #print(f"ans1 = {ans1}, ans2 = {ans2}")
            if get_levenshtein_distance(string1, string2)<5:
             #   print(f"{string1} : {string2}")
                prob1 = 0
                prob2 = 0
                if(ind>1):
                    #print(f"Pair1 = {arr[ind-1]}, {string2}")
                    prob1 = model[arr[ind-1]][string2]
                    #print(f"Prob1 = {prob1}")
                if(ind<len(arr)-1):
                    #print(f"Pair2 = {string2}, {arr[ind+1]}")
                    prob2 = model[string2][arr[ind+1]]
                    #print(f"Prob2 = {prob2}")
                if ind and ind<len(arr)-1:
                    if prob1 and prob2:
                        print(f"{arr[:ind]}, {string2}, {arr[ind+1:]}")
                elif ind:
                    if prob1 :
                        print(f"{arr[:ind]}, {string2}, {arr[ind+1:]}")
                elif ind<len(arr)-1:
                    if prob2:
                        print(f"{arr[:ind]}, {string2}, {arr[ind+1:]}")
