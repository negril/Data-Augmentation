## Author : Sandeep Ramachandra, sandeep.ramachandra@student.uni-siegen.de
## Description : Python file containing Self attention based generator(transformer generator) of GAN network

import torch
import torch.nn as nn
import numpy as np
import dataset
from EncodeLayer import EncodeLayer

class Generator(nn.Module):
    
    def __init__(self, noise_len = 100, output_size = (27,100), nheads = 3, period = 50, dim_feedforward = 2048, num_layers = 2):
        super(Generator,self).__init__()
        
        self.output_size = output_size
        self.noise_len = noise_len
        flat_output_size = np.prod(output_size)
        
        self.embedding = nn.Conv1d(noise_len, noise_len, 1)
        
        self.positional_embedding = dataset.generate_pe(1, noise_len, period = period)
        
        self.layer = nn.Sequential(
            *[EncodeLayer(d_model = noise_len, nhead = nheads, dim_feedforward = dim_feedforward, dropout = 0.5) for _ in range(num_layers)],
        )
        
        self.fcn = nn.Sequential(nn.PReLU(), nn.Dropout(0.4),
                                nn.Conv1d(noise_len, flat_output_size, 1)
                                )
        
        
    def forward(self, x):
        batch_size = x.shape[0]
        y = self.embedding(x.view(batch_size, -1, 1))
        y = y.view(batch_size, 1, self.noise_len) + self.positional_embedding.to(y.device) # broadcasting on batch dimension
        y = self.layer(y.view(batch_size, 1, self.noise_len))
        y = self.fcn(y.view(batch_size, -1, 1))
        y = y.view([batch_size]+list(self.output_size))
        return y
