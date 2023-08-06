from convblock import ConvBlock
import torch
import numpy as np
import autodl
from torch import nn

class TestModel(nn.Module):
    def __init__(self):
        super(TestModel, self).__init__()
        self.conv = torch.nn.Conv2d(3, 32, 3, 1)
        self.block1 = ConvBlock()
        self.block2 = ConvBlock()
        
    def forward(self, x):
        return self.block2(self.block1(self.conv(x)))

dummy_input = torch.randn(1, 3, 28, 28)
#just for testing prediction on server
np.save("inp.npy", dummy_input.numpy())
model = TestModel()

autodl.attach_model(model, dummy_input)
