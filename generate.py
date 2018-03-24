import argparse
import sys
import random


# freq[word1] = {word2 : number of pairs {word1, word2} in the corpus}
model = dict()


def load_model(instream):
    """Load the model.
    :param instream: pointer to the file with the model
    :return: None; the model is saved to the dictionary "model"
    """
    for line in instream.readlines():
        elems = line.split()
        if elems[0] not in model:
            model[elems[0]] = dict()
        for i in range(1, len(elems), 2):
            model[elems[0]][elems[i]] = int(elems[i + 1])


def generate(outstream, seed, length):
    """Generate a new text.
    :param outstream: pointer to an output file; stdout if none is specified
    :param seed: the desired first word
    :param length: length of output
    :return: None; the text is saved to the file pointed to by outstream
    """
    while length > 0:
        outstream.write(seed + ' ')
        if seed not in model:
            seed = random.choice(list(model.keys()))
        freq_list = []
        for word in model[seed]:
            for iter in range(model[seed][word]):
                freq_list.append(word)
        if len(freq_list) > 0:
            seed = random.choice(freq_list)
        else:
            seed = random.choice(list(model.keys()))
        length -= 1
    outstream.write('\n')


# creating a parser for parsing command line arguments
parser = argparse.ArgumentParser(
    description="Generate a new text on the base of corpus")
parser.add_argument("--model", help="Path to the file with generated model")
parser.add_argument("--seed", help="The desired first word;"\
                                   " will be chosen randomly by default")
parser.add_argument("--length", help="The desired length of text")
parser.add_argument("--output", help="File in which to save generated text"\
                                     "will be printed to stdout by default")
args = parser.parse_args()

instream = open(args.model, "r")
load_model(instream)
instream.close()

# if the user hasn't specified the first word,
# then select it randomly from all words in the corpus
if args.seed is None:
    args.seed = random.choice(list(model.keys()))

# if
if args.output is None:
    generate(sys.stdout, args.seed, int(args.length))
else:
    outstream = open(args.output, "w")
    generate(outstream, args.seed, int(args.length))
    outstream.close()