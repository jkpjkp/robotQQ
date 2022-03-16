import json
import random
import pypinyin


def getAllIdiomDetail():
    file = open('data/idiom.json', 'r', encoding='utf-8')
    s = json.load(file)
    return s


def getAnyIdiomDetail():
    file = open('data/idiom.json', 'r', encoding='utf-8')
    s = json.load(file)
    return s[getRandom()]


def getAnyIdiomWord():
    file = open('data/idiom.json', 'r', encoding='utf-8')
    s = json.load(file)
    return s[getRandom()]['word']


def getRandom():
    return random.randint(0, 30894)

if __name__ == '__main__':
    for dd in getAllIdiomDetail():
        word = dd['word']
        print(word)
        if pypinyin.lazy_pinyin(dd['word'][0])[0] == 'cang':
            print('-----------------------')
            break
