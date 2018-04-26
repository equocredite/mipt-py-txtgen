import argparse
import sys
import os
import re


def process_file(instream, lc, model):
    """Read a file, add to model.
    :param instream: pointer to an input file
    :param lc: True to make all letters lowercase
    :param model: where to save the model,
                  dictionary(string : dictionary(string : int))
    """
    # so that we could consider a pair separated by a newline character
    regex = re.compile("[^a-zA-Zа-яА-Я ]")
    previous_line_end = ""
    for line in instream:
        if lc:
            line = line.lower()
        # parse the words, throw out all non-alphabetic symbols
        words = (previous_line_end + regex.sub('', line)).split()
        for i in range(len(words) - 1):
            model.setdefault(words[i], dict())
            model[words[i]].setdefault(words[i + 1], 0)
            model[words[i]][words[i + 1]] += 1
        previous_line_end = words[-1]


def save_model(outstream, model):
    """Save the model.
    :param outstream: pointer to the file in which to save the model
    :param model: well, the model itself
    """
    for i in model:
        outstream.write(i + ' ')
        for j in model[i]:
            outstream.write(j + ' ' + str(model[i][j]) + ' ')
        outstream.write('\n')


def create_parser():
    """Create a parser, return it
    :return: a parser that can parse command line arguments (wow)
    """
    parser = argparse.ArgumentParser(
        description="Count frequencies of all pairs in"
                    " a corpus and save them")
    parser.add_argument("--input-dir",
                        help="Path to the folder with some texts to train on")
    parser.add_argument("--model",
                        help="Path to the file"
                             "in which the model shall be saved")
    parser.add_argument("--lc", action="store_true",
                        help="Make all letters lowercase")
    return parser


def run():
    args = create_parser().parse_args()

    # model[word1] = {word2 : number of pairs {word1, word2} in the corpus}
    model = dict()

    # if an input directory hasn't been specified,
    # then read the corpus from stdin
    if args.input_dir is None:
        process_file(sys.stdin, args.lc, model)
    else:
        # iterate over all files in the input directory
        for file_name in os.listdir(args.input_dir):
            instream = open(args.input_dir + "/" + file_name, "r")
            process_file(instream, args.lc, model)
            instream.close()

    outstream = open(args.model, "w")
    save_model(outstream, model)
    outstream.close()


if __name__ == "__main__":
    run()
