import sys
sys.path.append("../..")
import torch
import torch.nn as nn
import utils
from utils import END_TOKEN, UNKNOWN_TOKEN

class seq2seq(nn.Module):
    def __init__(self, post_embeddings, comment_embeddings, device):
        super().__init__()
        self.post_embeddings = post_embeddings
        self.comment_embeddings = comment_embeddings
        self.encoder = Encoder(self.post_embeddings)
        self.decoder = Decoder(self.comment_embeddings)
        self.device = device
    
    def forward(self, encoded_post_body, encoded_target_comment, tf_ratio=0.5):
        embedded = self.post_embeddings(encoded_post_body)
        out, context = self.encoder(embedded)
        
        return context

class Encoder(nn.Module):
    def __init__(self, post_embeddings):
        super().__init__()
        self.post_embeddings = post_embeddings
        self.encoder = nn.GRU(30, 1200, 2, batch_first=True, bidirectional=False)
        
    def forward(self, x):
        embedded = self.post_embeddings(x)
        # push vector through encoder
        # then take just the hidden vectors as the context vectors
        out, h_n = self.encoder(embedded)

        return h_n

# only for proof of concept-- cant work with batches
class Decoder(nn.Module):
    def __init__(self, comment_embeddings):
        super().__init__()
        self.comment_embeddings = comment_embeddings
        self.decoder = nn.GRU(30, 1200, 2, batch_first=True, bidirectional=False)
        self.fc = nn.Linear(1200, comment_embeddings.num_embeddings)

    def forward(self, context, last_output_word):
        """
        Since this function gets called once at a time rather than taking in
        a sequence of vectors, we need to pass it the last output. This will be just
        a vector of numbers that can be converted to the embedding representing that last output
        """
        embedded = self.comment_embeddings(last_output_word)
        out, h_n = self.decoder(context, embedded)

        return self.fc(h_n), h_n
