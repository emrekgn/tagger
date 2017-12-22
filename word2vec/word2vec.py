import gensim
import os
import re


class Tweets(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                # Replace URLs, convert to lowercase, strip and split by space...
                yield self.replace_urls(line.lower()).strip().split()

    @staticmethod
    def replace_urls(self, string):
        return re.sub(r'^https?:\/\/.*[\r\n ]*', 'URL', string, flags=re.MULTILINE)


tweets = Tweets('./dataset')
# Use skip-gram algorithm with negative sampling
model = gensim.models.Word2Vec(tweets, sg=1, min_count=4, size=200, workers=4, window=5)
