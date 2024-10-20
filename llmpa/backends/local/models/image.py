import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, efficientnet_v2_s

from transformers import AutoModel, AutoFeatureExtractor

# from tensorflow.keras.applications import (
#     EfficientNetV2B0,
#     ResNet50,
# )


# EmbeddingExtractor Class with model name as a parameter
class EmbeddingExtractor:
    def __init__(self, model_name="EfficientNetV2B0"):
        self.model_name = model_name
        self.use_pretrained_model = False
        self.feature_extractor = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.load_model()

    def load_model(self):
        if self.model_name == "EfficientNetV2B0":
            from torchvision.models import EfficientNet_V2_S_Weights

            base_model = efficientnet_v2_s(weights=EfficientNet_V2_S_Weights.DEFAULT)
            self.model = torch.nn.Sequential(*list(base_model.children())[:-1]).to(
                self.device
            )
        elif self.model_name == "ResNet50":
            from torchvision.models import ResNet50_Weights

            base_model = resnet50(weights=ResNet50_Weights.DEFAULT)
            self.model = torch.nn.Sequential(*list(base_model.children())[:-1]).to(
                self.device
            )
        else:
            self.use_pretrained_model = True
            self.feature_extractor = AutoFeatureExtractor.from_pretrained(
                self.model_name
            )
            self.model = AutoModel.from_pretrained(self.model_name).to(self.device)

    def preprocess_image(self, image):
        if self.use_pretrained_model:
            # If using Hugging Face models, do not apply torchvision transforms
            if image.shape[-1] == 3:  # Ensure 3 channels for RGB
                image = cv2.resize(image, (2048, 2048))  # Adjust size as needed
                image = np.expand_dims(image, axis=0)  # Add batch dimension
                return image
            else:
                raise ValueError(
                    f"Expected 3 channels (RGB) but got {image.shape[-1]} channels."
                )
        else:
            transform = transforms.Compose(
                [
                    transforms.ToTensor(),
                    transforms.Resize((2048, 2048)),  # Adjust size as needed
                    transforms.Normalize(
                        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                    ),
                ]
            )
            image = transform(image)
            image = image.unsqueeze(0).to(self.device)
            return image

    def extract_image_embedding(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = self.preprocess_image(image)
            with torch.no_grad():
                if self.use_pretrained_model:
                    inputs = self.feature_extractor(
                        images=image, return_tensors="pt"
                    ).to(self.device)
                    embedding = self.model(**inputs).last_hidden_state
                    return embedding.cpu().numpy().squeeze()
                else:
                    embedding = self.model(image).squeeze()
                    return embedding.cpu().numpy()
        return None

    def process_image(self, file_path):
        embedding = self.extract_image_embedding(file_path)
        if embedding is not None:
            print(f"Extracted embedding for image {file_path}: {embedding.shape}")
        else:
            print(f"Failed to extract embedding for image {file_path}")
        return embedding


if __name__ == "__main__":
    import os
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: {os.path.basename(__file__)} <filepath>")
        sys.exit(1)

    image_path = sys.argv[1]

    def test_model(model_name):
        extractor = EmbeddingExtractor(model_name=model_name)
        extractor.process_image(image_path)

    # Pass the model name as a parameter
    for model_name in [
        "EfficientNetV2B0",  ## embedding.shape == (1280,)
        "ResNet50",  ## embedding.shape == (2048,)
        "microsoft/resnet-50",  # Example for Hugging Face model
    ]:
        print(f"Testing model: {model_name}")
        test_model(model_name)
