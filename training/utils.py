"""
Utility functions to help with dataloading and preprocessing
"""

import pandas as pd

import nltk
# pretrained tokenizer
nltk.download('punkt')
from nltk.tokenize import word_tokenize 

__author__ = "Sander Schulhoff"
__email__ = "sanderschulhoff@gmail.com"

def read_json(path):
    return pd.read_json(path)

def preprocess(df, binary_classes=True):
    """
    tokenizes and encodes class numerically

    :param binary_classes: If True, considers YTA and ESH to be the same 
        class (1) and NTA and NAH to be the same class (0)
    """

    # Select columns to apply preprocessing to
    pp_cols = ["title", "body", "comment_body"]

    # tokenize data
    df[pp_cols] = df[pp_cols].applymap(lambda s:word_tokenize(s))

    # combine title and body of post
    df["body"] = df["title"] + df["body"]

    # get rid of now redundant title column
    df.drop(columns=["title"], axis=1, inplace=True)

    if binary_classes:
        df["judgement"] = df["judgement"].map({"YTA":1, "ESH":1, "NTA":0, "NAH":0})
    else:
        raise "deal with this later"
        
    return df

def gen_vocabulary(df, min_count=4, comment=True):
    """
    Generate a list of unique words in the corpus
    
    :param int min_count: The minimum # of occurences of word to be included in
        the list
    :param bool comment: If true, will additionally use text in comment bodies     
    """
    vocabulary = {}
    # count how many of each word occur
    def dmap(arr):
        for word in arr:
            if word in vocabulary:
                vocabulary[word]+=1
            else:
                vocabulary[word]=1

    df["body"].apply(lambda arr: dmap(arr))

    if comment:
        df["comment_body"].apply(lambda arr: dmap(arr))

    # remove all keys which occur less than 3 times
    vocabulary = {key : count for key, count in vocabulary.items() if count >= min_count}

    vocabulary =  list(vocabulary)

    # append special tokens
    # vocabulary += ["<UNK>", "<BEG>", "<END>"]

    return vocabulary


if __name__ == "__main__":
    df = read_json("example.json")

    df = preprocess(df)

    gen_vocabulary(df, 4)
