import utils
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
import pandas as pd

"""
Dataset and dataloader. Can be used to sample from dataset.
"""

__author__ = "Luke Luo"
__email__= "lluo6658@gmail.com"

"""
ID: post_body
label: comment_body

Both are stored in tokenized form
"""
class AITA_Dataset(Dataset):
    def __init__(self, list_ids, list_labels):
        self.list_ids = list_ids
        self.list_labels = list_labels
        
    def __len__(self):
        return len(self.list_labels)
    
    def __getitem__(self, idx):
        X = self.list_ids[idx]
        y = self.list_labels[idx]

        return X, y

    
"""
Creates a Dataset using post_body and comment_body columns of dataframe
"""
def get_dataloader(df):
    ds = AITA_Dataset(df.post_body, df.comment_body)
    
    loader = DataLoader(ds, batch_size=1, shuffle=True)
    
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