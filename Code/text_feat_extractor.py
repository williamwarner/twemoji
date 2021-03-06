"""
    One of the main parts of the main pipeline, the feature extractor
    class is used to extract a series of features for the data based
    on a specified loadout.
"""
# Imports
from sklearn.feature_extraction.text import CountVectorizer
from sentiment_lexicon_scoring import emolex_score
from sentiment_lexicon_scoring import sentiwordnet_score
from sentiment_lexicon_scoring import sentiwordnet_classify


class TextFeatureExtractor():
    """ A class to extract text features """
    def __init__(self):
        # A mapping of keywords to functions (for use in extract features)
        self.features_dict = {'unigram': self.unigram_features,
                              'bigram': self.bigram_features,
                              'trigram': self.trigram_features,
                              'emolex': self.emolex_features,
                              'swn_reg': self.swn_reg_features,
                              'swn_class': self.swn_class_features}

        # A list of the CV's trained (for pickling)
        self.pickleables = {}

    def unigram_features(self, data, cvargs, pickles):
        if pickles is None:
            if cvargs is not None:
                count_vect = CountVectorizer(
                    lowercase=cvargs['lowercase'],
                    stop_words=cvargs['stop_words'],
                    strip_accents=cvargs['strip_accents'],
                    token_pattern=cvargs['token_pattern']
                )
            else:
                count_vect = CountVectorizer()

            counts = count_vect.fit_transform(data)
            self.pickleables['unigram'] = count_vect  # store after fitting

        else:
            counts = pickles['unigram'].transform(data)

        return counts

    def bigram_features(self, data, cvargs, pickles):
        if pickles is None:
            if cvargs is not None:
                count_vect = CountVectorizer(
                    ngram_range=(2, 2),
                    lowercase=cvargs['lowercase'],
                    stop_words=cvargs['stop_words'],
                    strip_accents=cvargs['strip_accents'],
                    token_pattern=cvargs['token_pattern']
                )
            else:
                count_vect = CountVectorizer(ngram_range=(2, 2))

            counts = count_vect.fit_transform(data)
            self.pickleables['bigram'] = count_vect  # store after fitting

        else:
            counts = pickles['bigram'].transform(data)

        return counts
        
    def trigram_features(self, data, cvargs, pickles):
        if pickles is None:
            if cvargs is not None:
                count_vect = CountVectorizer(
                    ngram_range=(3, 3),
                    lowercase=cvargs['lowercase'],
                    stop_words=cvargs['stop_words'],
                    strip_accents=cvargs['strip_accents'],
                    token_pattern=cvargs['token_pattern']
                )
            else:
                count_vect = CountVectorizer(ngram_range=(3, 3))

            counts = count_vect.fit_transform(data)
            self.pickleables['trigram'] = count_vect  # store after fitting

        else:
            counts = pickles['trigram'].transform(data)

        return counts

    def emolex_features(self, data, cvargs, pickles):
        return emolex_score(data)

    def swn_reg_features(self, data, cvargs, pickles):
        feats = sentiwordnet_score(data)
        return feats.reshape(-1, 1)

    def swn_class_features(self, data, cvargs, pickles):
        feats = sentiwordnet_classify(data)
        return feats.reshape(-1, 1)

    def extract_features(self, data, features_to_extract,
                         cvargs=None, pickles=None):
        """ External function to call to extract multiple features

            ie:
                features_to_extract = ['unigram', 'bigram']
                would extract both feats and save to FE
        """

        features = {}
        for feat in features_to_extract:
            print "Extracting feature", feat
            features[feat] = self.features_dict[feat](data, cvargs, pickles)

        return features

    def get_pickleables(self):
        """ Returns the parts of TFE needed to pickle

            Currently this is only a list of the fitted CV's used!
        """
        return self.pickleables
