#!/usr/bin/env python

import os
import optparse
import re

dataset_path = "../dataset"
dataset_conll_path = os.path.join(dataset_path, "conll2003")

# Read parameters from command line
optparser = optparse.OptionParser()
optparser.add_option(
    "-m", "--muc", default="../dataset/tr.twitter50K.MUClabeled",
    help="Location of MUC labelled input file"
)
optparser.add_option(
    "-i", "--ignore_mentions", default="0",
    type='int', help="Ignore tweet mentions (default 0)"
)
opts = optparser.parse_args()[0]

# Check parameters validity
assert os.path.isfile(opts.muc)

# Check dataset folder
if not os.path.exists(dataset_conll_path):
    os.makedirs(dataset_conll_path)

with open(opts.muc, "r") as muc, open(os.path.join(dataset_conll_path, "input.txt"), "w+") as conll:
    numb_label = 0
    for c, line in enumerate(muc):
        tokens = line.strip().split()
        is_label = False
        iobes_tag = None
        prev_label_type = None
        for i, token in enumerate(tokens):
            if 'b_enamex' in token:
                is_label = True
                iobes_tag = None
                prev_label_type = None
                numb_label += 1
                continue
            if is_label:
                if 'e_enamex' in token:
                    search_result = re.search(r'TYPE=\"(PERSON|ORGANIZATION|LOCATION)\">(.*)<e_enamex>', token)
                    # Singleton label
                    if search_result:
                        groups = search_result.groups()
                        if groups and len(groups) == 2:
                            label_type = groups[0]
                            new_token = str(groups[1]).strip()
                            iobes_tag = "S"
                            if opts.ignore_mentions == 1 and str.startswith(new_token, '@'):
                                conll.write(new_token + " O\n")
                            else:
                                conll.write("{0} {1}-{2}\n".format(new_token, iobes_tag, label_type))
                    # End label
                    else:
                        search_result = re.search(r'(.*)<e_enamex>', token)
                        if search_result:
                            groups = search_result.groups()
                            if groups and len(groups) == 1:
                                label_type = prev_label_type
                                new_token = groups[0]
                                iobes_tag = "E"
                                conll.write("{0} {1}-{2}\n".format(new_token, iobes_tag, label_type))
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
                        conll.write("{0} {1}-{2}\n".format(new_token, iobes_tag, label_type))
                # Inside label
                elif iobes_tag == "B" and prev_label_type:
                    iobes_tag = "I"
                    conll.write("{0} {1}-{2}\n".format(token, iobes_tag, prev_label_type))
            else:
                conll.write(token + " O\n")
        conll.write("\n")
    print("Number of tweets: {0} Number of named entities: {1}".format(c, numb_label))
