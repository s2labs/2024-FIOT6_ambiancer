"""
VGG11/13/16/19 in Pytorch.
Credits: https://github.com/Lornatang/VGG-PyTorch
"""

import torch.nn as nn
import torch.nn.functional as F

# Configuration dictionary for different VGG variants
configs = {
    'VGG11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG13': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'VGG19': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}

def _make_layers(config):
    """
    Creates the layers for the VGG network based on the provided configuration.

    Args:
        config (list): A list defining the configuration of the VGG network.

    Returns:
        nn.Sequential: A sequential container of the layers.
    """
    layers = []
    in_channels = 3
    for x in config:
        if x == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            layers += [nn.Conv2d(in_channels, x, kernel_size=3, padding=1),
                       nn.BatchNorm2d(x),
                       nn.ReLU(inplace=True)]
            in_channels = x
    layers += [nn.AvgPool2d(kernel_size=1, stride=1)]
    return nn.Sequential(*layers)

class VGG(nn.Module):
    """
    VGG model class.

    Args:
        vgg_name (str): The name of the VGG variant to use (e.g., 'VGG11', 'VGG13', 'VGG16', 'VGG19').

    Attributes:
        features (nn.Sequential): The feature extraction layers.
        classifier (nn.Linear): The classification layer.
    """
    def __init__(self, vgg_name):
        super(VGG, self).__init__()
        self.features = _make_layers(configs[vgg_name])
        self.classifier = nn.Linear(512, 7)

    def forward(self, x):
        """
        Defines the forward pass of the VGG model.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor after passing through the network.
        """
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = F.dropout(out, p=0.5, training=self.training)
        out = self.classifier(out)
        return out