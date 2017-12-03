#!/usr/bin/env python

import os
import optparse
import numpy as np

dataset_path = "../dataset"
dataset_conll_path = os.path.join(dataset_path, "conll2003")

# Read parameters from command line
optparser = optparse.OptionParser()
optparser.add_option(
    "-c", "--conll", default="",
    help="Location of Conll2003 labelled input file"
)
opts = optparser.parse_args()[0]

# Check parameters validity
assert os.path.isfile(opts.muc)

# Check dataset folder
if not os.path.exists(dataset_conll_path):
    os.makedirs(dataset_conll_path)

train, validate, test = np.split