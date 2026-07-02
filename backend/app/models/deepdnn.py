import torch
import torch.nn as nn


class VirulenceDNN(nn.Module):

    def __init__(self, input_dim):
        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(input_dim, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.4),

            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(256, 1),
            nn.Sigmoid()

        )

    def forward(self, x):
        return self.network(x)