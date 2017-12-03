#!/usr/bin/env python

import os
import optparse
import re

dataset_path = "../dataset"
dataset_conll_path = os.path.join(dataset_path, "conll2003")

# Read parameters from command line
optparser = optparse.OptionParser()
optparser.add_option(
    "-m", "--muc", default="",
    help="Location of MUC labelled input file"
)
opts = optparser.parse_args()[0]

# Check parameters validity
assert os.path.isfile(opts.muc)

# Check dataset folder
if not os.path.exists(dataset_conll_path):
    os.makedirs(dataset_conll_path)

with open(opts.muc, "r") as muc, open(os.path.join(dataset_conll_path, "input.txt"), "w+") as conll:
    for line in muc:
        tokens = line.strip().split()
        is_label = False
        iobes_tag = None
        prev_label_type = None
        for i, token in enumerate(tokens):
            if 'b_enamex' in token:
                is_label = True
                iobes_tag = None
                prev_label_type = None
                continue
            if is_label:
                if 'e_enamex' in token:
                    search_result = re.search(r'TYPE=\"(PERSON|ORGANIZATION|LOCATION)\">(.*)<e_enamex>', token)
                    # Singleton label
                    if search_result:
                        groups = search_result.groups()
                        if groups and len(groups) == 2:
                            label_type = groups[0]
                            new_token = groups[1]
                            iobes_tag = "S"
                            conll.write("{0} {1}_{2}\n".format(new_token, iobes_tag, label_type))
                    # End label
                    else:
                        search_result = re.search(r'(.*)<e_enamex>', token)
                        if search_result:
                            groups = search_result.groups()
                            if groups and len(groups) == 1:
                                label_type = prev_label_type
                                new_token = groups[0]
                                iobes_tag = "E"
                                conll.write("{0} {1}_{2}\n".format(new_token, iobes_tag, label_type))
                    is_label = False
                # Begin label
                elif iobes_tag is None:
                    search_result = re.search(r'TYPE=\"(PERSON|ORGANIZATION|LOCATION)\">(.*)', token)
                    if search_result:
                        groups = search_result.groups()
                        label_type = groups[0]
                        prev_label_type = label_type
                        new_token = groups[1]
                        iobes_tag = "B"
                        conll.write("{0} {1}_{2}\n".format(new_token, iobes_tag, label_type))
                elif iobes_tag == "B" and prev_label_type:
                    conll.write("{0} {1}_{2}\n".format(token, iobes_tag, prev_label_type))
            else:
                conll.write(token + " O\n")
        conll.write("\n")
