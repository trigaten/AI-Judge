import utils
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
import pandas as pd

"""
Dataset and dataloader. Can be used to sample from dataset.
"""

__authors__ = ["Luke Luo", "Sander Schulhoff"]
__email__= "lluo6658@gmail.com"

START_TOKEN = "<BEG>"
END_TOKEN = "<END>"
UNKNOWN_TOKEN = "<UNK>"

"""
ID: post_body
label: comment_body

Both are stored in tokenized form
"""
class AITA_Dataset(Dataset):
    def __init__(self, df, vocabulary):
        """
        :param df: a pandas dataframe
        :param vocabulary: a list or dictionary strings
        """
        self.list_ids = df['post_body']
        self.list_labels = df['comment_body']
        self.vocabulary = vocabulary

    def __len__(self):
        return len(self.list_labels)
    
    def __getitem__(self, idx):
        """
        Return a tuple of lists of strings
        """
        X = self.list_ids[idx]
        y = self.list_labels[idx]
        return self.apply_special_tokens(X), self.apply_special_tokens(y)

    def apply_special_tokens(self, sentence):
        """
        Adds begin and end tokens. Also replaces words not in 
        vocabulary with unknown token
        :param sentence: a list of words
        """
        for i, word in enumerate(sentence):
            if word not in self.vocabulary:
                sentence[i] = UNKNOWN_TOKEN

        return [START_TOKEN] + sentence + [END_TOKEN]

"""
Creates a Dataset using post_body and comment_body columns of dataframe
"""
def get_dataloader(df):
    ds = AITA_Dataset(df)
    
    loader = DataLoader(ds, batch_size=5, shuffle=True)
    
    return loader


"""
Samples a single post as a dataframe and unpacks the tuples
"""
def sample_dl(dl):
    train_features, train_labels = enumerate(next(iter(dl)))
    post = pd.DataFrame([train_features, train_labels], ['post_body', 'comment_body'])
    post = post.drop(0, 1)
    post = post.transpose()
    
    list1, list2 = [], []
    for i in range(len(post.post_body[1])):
        list1.append(post.post_body[1][i][0])
    for i in range(len(post.comment_body[1])):
        list2.append(post.comment_body[1][i][0])
    post.post_body[1] = list1
    post.comment_body[1] = list2
    
    return post
