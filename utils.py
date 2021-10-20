"""Utility functions to help with dataloading and preprocessing"""

import pandas as pd

import nltk
# pretrained tokenizer
nltk.download('punkt')
from nltk.tokenize import word_tokenize 

__author__ = "Sander Schulhoff"
__email__ = "sanderschulhoff@gmail.com"

def read_json(path):
    return pd.read_json(path)

def tokenize_df(df):
    # Select columns to apply preprocessing to
    pp_cols = ["title", "body", "comment_body"]

    # tokenize data
    df[pp_cols] = df[pp_cols].applymap(lambda s:word_tokenize(s))

    # combine title and body of post
    df["body"] = df["title"] + df["body"]

    # get rid of now redundant title column
    df.drop(columns=["title"], axis=1, inplace=True)

    return df

if __name__ == "__main__":
    df = read_json("example.json")
    print(tokenize_df(df))
