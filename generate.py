import argparse
import sys
import random


def create_parser():
    """Create a parser, return it
    :return: quite unexpectedly, a parser that can parse arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate a new text on the base of corpus")
    parser.add_argument("--model",
                        help="Path to the file with generated model")
    parser.add_argument("--seed", help="The desired first word; "
                                       "will be chosen randomly by default")
    parser.add_argument("--length", help="The desired length of text")
    parser.add_argument("--output",
                        help="File in which to save generated text; "
                             "will be printed to stdout by default")
    return parser


def load_model(instream, model):
    """Load the model.
    :param instream: pointer to the file with the model
    :param model: where to load the model,
                  dictionary(string : dictionary(string : int))
    """
    for line in instream:
        elems = line.split()
        model.setdefault(elems[0], dict())
        for i in range(1, len(elems), 2):
            model[elems[0]][elems[i]] = int(elems[i + 1])


def generate(outstream, seed, length, model):
    """Generate a new text.
    :param outstream: pointer to an output file; stdout if none is specified
    :param seed: the desired first word
    :param length: length of output
    :param model: same as in documentation for load_model()
    """
    if seed not in model:
        seed = random.choice(list(model.keys()))
    while length > 0:
        outstream.write(seed + ' ')
        freq_sum = 0
        for word in model[seed]:
            freq_sum += model[seed][word]
        if freq_sum == 0:
            seed = random.choice(list(model.keys()))
        else:
            key = random.randint(1, freq_sum)
            cur = 0
            for word in model[seed]:
                cur += model[seed][word]
                if cur >= key:
                    seed = word
                    break
        length -= 1
    outstream.write('\n')


def run():
    args = create_parser().parse_args()

    # freq[word1] = {word2 : number of pairs {word1, word2} in the corpus}
    model = dict()

    instream = open(args.model, "r")
    load_model(instream, model)
    instream.close()

    # if the first word is not specified,
    # then select it randomly from all words in the corpus
    if args.seed is None:
        args.seed = random.choice(list(model.keys()))

    # if an output file hasn't been specified,
    # then print generated text to stdout
    if args.output is None:
        generate(sys.stdout, args.seed, int(args.length), model)
    else:
        outstream = open(args.output, "w")
        generate(outstream, args.seed, int(args.length), model)
        outstream.close()


if __name__ == "__main__":
    run()
