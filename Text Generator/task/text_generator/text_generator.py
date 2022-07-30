from nltk.tokenize import WhitespaceTokenizer
from nltk.util import bigrams, trigrams
from collections import Counter
import random
import re

file_name = input()


def main():
    with open(file_name) as f:
        wt = WhitespaceTokenizer()
        tok_file = wt.tokenize(f.read())
        # print(wt.tokenize(f.read()))
        # print("Corpus statistics")
        # print("All tokens:", len(tok_file))
        # print("Unique tokens:", len(set(tok_file)))

    bigram_file = list(bigrams(tok_file))
    trigram_file = list(trigrams(tok_file))
    # print(trigram_file)
    # print('Number of bigrams:', len(bigram_file))
    bigram_dict = {}
    for h, t in bigram_file:
        bigram_dict.setdefault(h, []).append(t)

    trigram_dict = {}
    for h, m, t in trigram_file:
        trigram_dict.setdefault(h + ' ' + m, []).append(t)
    sentences(tok_file, trigram_dict)


def sentences(tok_file, trigram_dict):

    list_head_words = re.findall(r"[A-Z][\w'-,]+\s[\w'-,.]+", ';'.join(trigram_dict.keys()))
    # list_head_words = re.findall(r"[A-Z][\w'-,]+", ' '.join(tok_file))
    list_end_words = re.findall(r"[\w'-,]+[.!?]", ' '.join(tok_file))

    for s in range(10):
        cnt = 2
        head_word = random.choice(list_head_words)
        sentence = head_word.split()

        while True:
            pair = Counter(trigram_dict[head_word])
            weights = list(pair.values())
            new_head_word = sentence[-1] + ' ' + random.choices(list(pair.keys()), weights=weights)[0]
            cnt += 1

            if cnt >= 5 and len(sentence) >= 4 and new_head_word.split()[-1] in list_end_words:
                sentence.append(new_head_word.split()[-1])
                break
            elif new_head_word.split()[-1] in list_end_words:
                if len(sentence) < 4:
                    sentence.append(new_head_word.split()[-1])
                    head_word = new_head_word
                    cnt = 0
                else:
                    continue
            else:
                sentence.append(new_head_word.split()[-1])
                head_word = new_head_word

        print(*sentence)


def bigrams_counts(bigram_dict):
    for key in iter(input, 'exit'):
        try:
            pair = Counter(bigram_dict[key]).most_common()
            print(f'Head: {key}')
            for k, v in pair:
                print(f'Tail: {k}   Count: {v}')
            print(f'Head: {pair[0]}     Tail: {pair[1]}')
        # except IndexError:
        #     print('Index Error. Please input a value that is not greater than the number of all bigrams.')
        # except ValueError:
        #     print('ValueError. Please input an integer.')
        except KeyError:
            print('Key Error. The requested word is not in the model. Please input another word.')


if __name__ == '__main__':
    main()
    