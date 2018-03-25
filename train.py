import argparse
import sys
import os


def process_file(instream, lc, model):
    """Read a file, save to freq.
    :param instream: pointer to an input file
    :param lc: True to make all letters lowercase
    :param model: where to save the model,
                  dictionary(string : dictionary(string : int))
    """
    # so that we could consider a pair separated by a newline character
    previous_line_end = ""
    for line in instream.readlines():
        # the same line, but with each
        # non-alphabetical symbol replaced with a space"""
        clean_line = previous_line_end + ' '
        for c in line:
            if c.isalpha():
                if lc:
                    c = c.lower()
                clean_line += c
            else:
                clean_line += ' '
        words = clean_line.split()
        for i in range(len(words) - 1):
            if words[i] not in model:
                model[words[i]] = dict()
            if words[i + 1] not in model[words[i]]:
                model[words[i]][words[i + 1]] = 0
            model[words[i]][words[i + 1]] += 1
        previous_line_end = words[len(words) - 1]


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


def get_args():
    """Create a parser, read arguments, return them"""
    parser = argparse.ArgumentParser(
        description="Count frequencies of all texts in a corpus and save them")
    parser.add_argument("--input-dir",
                        help="Path to the folder with some texts to train on")
    parser.add_argument("--model",
                        help="Path to the file"
                             "in which the model shall be saved")
    parser.add_argument("--lc", action="store_true",
                        help="Make all letters lowercase")
    return parser.parse_args()


def run():
    args = get_args()

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
