import utils
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
import pandas as pd
import utils

"""
Dataset and dataloader. Can be used to sample from dataset.
"""

__authors__ = ["Luke Luo", "Sander Schulhoff"]
__email__= "lluo6658@gmail.com"

"""
ID: post_body
label: comment_body

Both are stored in tokenized form
"""
class AITA_Dataset(Dataset):
    def __init__(self, df, post_vocab, comm_vocab):
        """
        :param df: a pandas dataframe
        :param vocabulary: a list or dictionary strings
        """
        self.list_ids = df['post_body']
        self.list_labels = df['comment_body']
        self.post_vocab = post_vocab
        self.comm_vocab = comm_vocab

    def __len__(self):
        return len(self.list_labels)
    
    def __getitem__(self, idx):
        """
        Return a tuple of lists of strings
        """
        X = self.list_ids[idx]
        y = self.list_labels[idx]
        # print(X)
        return self.apply_special_tokens(X, self.post_vocab), self.apply_special_tokens(y, self.comm_vocab)

    def apply_special_tokens(self, sentence, vocab):
        """
        Add begin and end tokens. Also replace words not in 
        vocabulary with unknown token
        :param sentence: a list of strings
        """
        for i, word in enumerate(sentence):
            if word not in vocab:
                sentence[i] = utils.UNKNOWN_TOKEN
        
        return [utils.START_TOKEN] + sentence + [utils.END_TOKEN]

"""
Collator function to be called with dataloader
"""
def collator(batch):

    ids = (x[0] for x in batch)
    labels = (x[1] for x in batch)
    
    id_lengths = [len(sentence) for sentence in ids]
    label_lengths = [len(sentence) for sentence in labels]
    
    id_longest = max(id_lengths)
    id_batch_size = len(id_lengths)
    padded_ids = np.ones((id_batch_size, 0)).tolist()
    
    label_longest = max(label_lengths)
    label_batch_size = len(label_lengths)
    padded_labels = np.ones((label_batch_size, 0)).tolist()
     
    # pad ids
    
    for i, length in enumerate(id_lengths):
        sequence = batch[i][0]
        for n in range(length, id_longest):
            sequence.append(utils.PAD_TOKEN)

        padded_ids[i].append(sequence)
        padded_ids[i] = padded_ids[i][0]
            
    # pad labels
                            
    for i, length in enumerate(label_lengths):
        sequence = batch[i][1]
        for n in range(length, label_longest):
            sequence.append(utils.PAD_TOKEN)
        
        padded_labels[i].append(sequence)
        padded_labels[i] = padded_labels[i][0]
               
    return (padded_ids, padded_labels)

"""
Creates a Dataset using post_body and comment_body columns of dataframe
"""
def get_dataloader(df, vocab, batch_size=5):
    ds = AITA_Dataset(df, vocab)
    
    loader = DataLoader(ds, batch_size=batch_size, shuffle=True, collate_fn=collator)
    
    return loader


"""
Samples a single post as a dataframe and unpacks the tuples
"""
def sample_dl(dl):
    features, labels = next(iter(loader))
    
    batch = pd.DataFrame([features, labels], ['post_body', 'comment_body'])
    batch = batch.drop(0, 1)
    batch = batch.transpose()
    
    return batch

