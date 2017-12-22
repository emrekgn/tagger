#!/usr/bin/env python

import os
import optparse
import numpy as np

dataset_path = "../dataset"
dataset_conll_path = os.path.join(dataset_path, "conll2003")

# Read parameters from command line
optparser = optparse.OptionParser()
optparser.add_option(
    "-c", "--conll", default="../dataset/conll2003/input.txt",
    help="Location of Conll2003 labelled input file"
)
optparser.add_option(
    "-e", "--examples", default="5040",
    help="Total number of examples"
)
optparser.add_option(
    "-t", "--train", default="60",
    help="Desired percentage of train examples"
)
optparser.add_option(
    "-d", "--dev", default="20",
    help="Desired percentage of development examples"
)
optparser.add_option(
    "-v", "--valid", default="20",
    help="Desired percentage of validation examples"
)
opts = optparser.parse_args()[0]

# Check parameters validity
assert os.path.isfile(opts.conll)

# Check dataset folder
if not os.path.exists(dataset_conll_path):
    os.makedirs(dataset_conll_path)

with open(opts.conll, "r") as conll, open(os.path.join(dataset_conll_path, "train.txt"), "w+") as train_file, \
    open(os.path.join(dataset_conll_path, "dev.txt"), "w+") as dev_file, \
        open(os.path.join(dataset_conll_path, "test.txt"), "w+") as test_file:
    # Initialize counters
    numb_train = int(round(int(opts.examples) * (float(opts.train) / 100)))
    count_train = 0
    numb_dev = int(round(int(opts.examples) * (float(opts.dev) / 100)))
    count_dev = 0
    numb_test = int(round(int(opts.examples) * (float(opts.valid) / 100)))
    count_test = 0

    # Group each tweet divided by empty line
    tweet = []
    for line in conll:
        if line.strip():
            tweet.append(line.strip())
        else:
            if count_train <= numb_train:
                train_file.write('{0}\n\n'.format('\n'.join(tweet)))
                count_train += 1
            elif count_test <= numb_test:
                test_file.write('{0}\n\n'.format('\n'.join(tweet)))
                count_test += 1
            elif count_dev <= numb_dev:
                dev_file.write('{0}\n\n'.format('\n'.join(tweet)))
                count_dev += 1
            tweet = []
