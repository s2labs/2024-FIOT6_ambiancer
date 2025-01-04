import torch
import torch.nn.functional as F
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
from vgg import VGG
from constants import CLASS_NAMES, WEIGHTS_PATH

# Define the transform using torchvision
transform_test = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),  # Convert to grayscale and keep 3 channels
    transforms.Resize((48, 48)),  # Resize to 48x48
    transforms.ToTensor(),  # Convert to tensor
])

def load_model():
    """
    Loads the VGG19 model with pre-trained weights.

    Returns:
        VGG: The VGG19 model loaded with pre-trained weights.
    """
    net = VGG('VGG19')
    checkpoint = torch.load(WEIGHTS_PATH, weights_only=True)
    net.load_state_dict(checkpoint['net'])
    net.cuda()
    net.eval()
    return net

def preprocess_image(image):
    """
    Preprocesses the input image for the VGG model.

    Args:
        image (numpy.ndarray): The input image in numpy array format.

    Returns:
        torch.Tensor: The preprocessed image tensor.
    """
    img = Image.fromarray(image)
    img = transform_test(img)
    return img

def predict(image, model):
    """
    Predicts the expression from the input image using the provided model.

    Args:
        image (numpy.ndarray): The input image in numpy array format.
        model (VGG): The VGG model to use for prediction.

    Returns:
        torch.Tensor: The raw output logits from the model.
    """
    inputs = preprocess_image(image)
    inputs = inputs.unsqueeze(0)  # Add batch dimension
    inputs = inputs.cuda()
    with torch.no_grad():
        inputs = Variable(inputs)
        outputs = model(inputs)
    return outputs

def get_expression(logits):
    """
    Converts the raw output logits to a human-readable expression.

    Args:
        logits (torch.Tensor): The raw output logits from the model.

    Returns:
        str: The predicted expression.
    """
    probs = F.softmax(logits, dim=1)
    max_prob, idx = torch.max(probs, 1)
    emotion = CLASS_NAMES[idx.item()]
    return emotion