"""
Utility functions to help with dataloading and preprocessing
"""

import pandas as pd

import nltk
# pretrained tokenizer
nltk.download('punkt')
from nltk.tokenize import word_tokenize 

from gensim.models import Word2Vec
from gensim import corpora

import torch
from torch.nn import Embedding

import numpy as np

MIN_WORD_COUNT = 4
START_TOKEN = "<BEG>"
END_TOKEN = "<END>"
UNKNOWN_TOKEN = "<UNK>"

__author__ = "Sander Schulhoff"
__email__ = "sanderschulhoff@gmail.com"

def read_json(path):
    return pd.read_json(path)

def preprocess(df, binary_classes=True):
    """
    Tokenizes and encodes class numerically

    :param binary_classes: If True, considers YTA and ESH to be the same 
        class (1) and NTA and NAH to be the same class (0)
    """

    # Select columns to apply preprocessing to
    pp_cols = ["title", "post_body", "comment_body"]
    
    # make all lowercase
    df[pp_cols] = df[pp_cols].applymap(lambda s:s.lower())
    
    # combine title and body of post
    df["post_body"] = df["post_body"].applymap(lambda x: x + " ")
    df["post_body"] = df["title"] + " " +  df["post_body"]

    # get rid of now redundant title column
    df.drop(columns=["title"], axis=1, inplace=True)

    # apply to post only

    # Remove all the special characters
    df["post_body"] = df["post_body"].applymap(lambda s:re.sub(r'\W', ' ',s))

    # remove all single characters
    df["post_body"] = df["post_body"].applymap(lambda s:re.sub(r'\s+[a-zA-Z]\s+', ' ',s))

    # Remove single characters from the start (no space before them, but space after)
    df["post_body"] = df["post_body"].applymap(lambda s:re.sub(r'^[a-zA-Z]\s+', ' ',s))

    # Removing prefixed 'b'
    df["post_body"] = df["post_body"].applymap(lambda s:re.sub(r'^b\s+', ' ',s,flags=re.I))

    # remove all of: x200b (zero-width space)
    df["post_body"] = df["post_body"].applymap(lambda s:re.sub(r'x200b', ' ',s))

    # Substituting multiple spaces with single space
    df["post_body"] = df["post_body"].applymap(lambda s:re.sub(r'\s+', ' ',s,flags=re.I))

    # Remove single numbers
    df["post_body"] = df["post_body"].applymap(lambda s:re.sub(r'\d+', ' ',s,flags=re.I))

    # remove stopwords
    df["post_body"] = df["post_body"].applymap(lambda s: [word for word in s if word not in stopwords.words('english')])
    
    # tokenize df
    df["post_body"] = df["post_body"].applymap(lambda s:word_tokenize(s))

    # perform stemming
    df["post_body"] = df["post_body"].applymap(lambda s: [ps.stem(word) for word in s])

     # tokenize data
    df[pp_cols] = df[pp_cols].applymap(lambda s:word_tokenize(s))    

    if binary_classes:
        df["judgement"] = df["judgement"].map({"YTA":1, "ESH":1, "NTA":0, "NAH":0})
    else:
        raise "deal with this later"
        
    return df

def gen_vocabulary(df, min_count=MIN_WORD_COUNT, comment=True):
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

    df["post_body"].apply(lambda arr: dmap(arr))

    if comment:
        df["comment_body"].apply(lambda arr: dmap(arr))

    # remove all keys which occur less than 3 times
    vocabulary = {key : count for key, count in vocabulary.items() if count >= min_count}

    vocabulary =  list(vocabulary)

    return vocabulary


"""
Functions which support the generation/saving/loading of embeddings.
"""

def train_embeddings(df, save_path=None, eps=1000):

    posts = list(df["post_body"])

    model = Word2Vec(sentences=posts, vector_size=30, epochs=eps, min_count=MIN_WORD_COUNT, window=2)

    if save_path:
        model.save(save_path)

    return model


def load_embeddings(save_path):
    """Abstract the loading process so don't need gensim calls in other files"""
    return Word2Vec.load(save_path)

def gensim_to_pytorch(gse):
    """
    Convert a gensim word2vec to a pytorch embedding
    :return: Tuple containing a word to index dictionary and the Pytorch embedding
    """
    word_to_idx = {word:index for index, word in enumerate(gse.wv.index_to_key)}
    weights = torch.FloatTensor([gse.wv.get_vector(word) for word in gse.wv.index_to_key])
    embed = Embedding.from_pretrained(weights)
    
    return word_to_idx, embed

def get_embeddings(path="embeddings_30_1000", special_tokens=True):
    gensim_embeds = load_embeddings(path)

    if special_tokens: 
        gensim_embeds.wv[START_TOKEN] = np.random.normal(0, 1, size=(gensim_embeds.vector_size))
        gensim_embeds.wv[END_TOKEN] = np.random.normal(0, 1, size=(gensim_embeds.vector_size))
        gensim_embeds.wv[UNKNOWN_TOKEN] = np.random.normal(0, 1, size=(gensim_embeds.vector_size))
    
    return gensim_to_pytorch(gensim_embeds)
    
if __name__ == "__main__":
    df = read_json("example.json")

    df = preprocess(df)

    # gen_vocabulary(df, MIN_WORD_COUNT)

    train_embeddings(df, "embeddings_30_1000")


