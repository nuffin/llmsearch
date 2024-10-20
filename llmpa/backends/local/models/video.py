import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models.video as models

import cv2
import numpy as np

from transformers import TFAutoModel  # For Hugging Face models

# from tensorflow.keras.models import load_model  # To load the converted X3D model


class EmbeddingExtractor:
    def __init__(
        self,
        model_name="EfficientNetV2B0",
        input_shape=(224, 224, 3),
        device="cuda" if torch.cuda.is_available() else "cpu",
    ):
        self.model_name = model_name
        self.input_shape = input_shape
        self.device = device
        self.model = self.load_model()

    def load_model(self):
        # Load the pre-trained X3D model from torchvision
        if self.model_name == "x3d_m":
            model = models.video.x3d_x3d_m(pretrained=True)
        elif self.model_name == "x3d_s":
            model = models.video.x3d_x3d_s(pretrained=True)
        elif self.model_name == "x3d_l":
            model = models.video.x3d_x3d_l(pretrained=True)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

        # Remove the final classification layer to extract embeddings
        model = nn.Sequential(*list(model.children())[:-1])
        model.to(self.device)
        model.eval()

        return model

    def preprocess_video_frames(self, frames):
        # Resize and normalize each frame to the input shape for X3D (3D CNN models expect normalization)
        transform = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize(self.input_shape),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.45, 0.45, 0.45], std=[0.225, 0.225, 0.225]
                ),
            ]
        )
        processed_frames = [transform(frame) for frame in frames]
        return torch.stack(
            processed_frames
        )  # Stack frames into a tensor (batch of frames)

    def extract_video_embeddings(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
        success = True
        frame_count = 0

        # Extract up to 90 frames
        while success and frame_count < 90:
            success, frame = cap.read()
            if success:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
            frame_count += 1

        cap.release()

        if len(frames) > 0:
            frames_tensor = (
                self.preprocess_video_frames(frames).unsqueeze(0).to(self.device)
            )  # Add batch dimension
            with torch.no_grad():
                embeddings = self.model(frames_tensor)
            return embeddings.squeeze().cpu().numpy()  # Convert to numpy array
        return None

    def process_video(self, file_path):
        embeddings = self.extract_video_embeddings(file_path)
        if embeddings is not None:
            print(f"Extracted embeddings for video {file_path}: {embeddings.shape}")
        else:
            print(f"Failed to extract embeddings for video {file_path}")
        return embeddings


if __name__ == "__main__":
    import os
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: {os.path.basename(__file__)} <filepath>")
        sys.exit(1)

    video_path = sys.argv[1]

    def test_model(model_name):
        extractor = EmbeddingExtractor(model_name=model_name)
        extractor.process_video(video_path)
