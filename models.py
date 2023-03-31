import torch
import torch.nn.functional as F

class RegressionLinear(torch.nn.Module):
    def __init__(self,in_features, out_features):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.network = torch.nn.Sequential(
            torch.nn.Linear(self.in_features, 100),
            torch.nn.ReLU(),
            torch.nn.Linear(100,  self.out_features),
        )

    def forward(self, x):
        return self.network(x)
