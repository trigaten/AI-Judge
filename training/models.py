import torch
import torch.nn as nn

class seq2seq(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.GRU(30, 1200, 3, batch_first=True, bidirectional=True)
        self.decoder = nn.GRU(30, 1200, 3, batch_first=True, bidirectional=True)
        
    def forward(x):
        return 0

# if __name__ == '__main__':
