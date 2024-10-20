import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models.video as models

# import tensorflow as tf
import cv2
import numpy as np

# from tensorflow.keras.applications import EfficientNetV2B0  # Replaceable with other models
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
        ## if self.model_name == "EfficientNetV2B0":
        ##     base_model = EfficientNetV2B0(include_top=False, pooling="avg")
        ##     model = tf.keras.Model(inputs=base_model.input, outputs=base_model.output)
        ## else if self.model_name == "x3d_model_tf":
        ##     # Load the converted X3D model
        ##     model = load_model(self.model_name)
        ## else:
        ##     # Load a model from Hugging Face if it's a supported video model
        ##     model = TFAutoModel.from_pretrained(self.model_name)
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
        ## Resize each frame to the input shape for the specific model
        # frames = [cv2.resize(frame, (self.input_shape[0], self.input_shape[1])) for frame in frames]
        # frames = np.array(frames).astype("float32") / 255.0  # Normalize to [0, 1]
        # return frames
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
            ## frames = self.preprocess_video_frames(frames)
            ## embeddings = self.model.predict(np.expand_dims(frames, axis=0))  # Add batch dimension
            ## return embeddings.squeeze()  # Return embedding as numpy array
            frames_tensor = (
                self.preprocess_video_frames(frames).unsqueeze(0).to(self.device)
            )  # Add batch dimension
            with torch.no_grad():
                embeddings = self.model(frames_tensor)
            return embeddings.squeeze().cpu().numpy()  # Convert to numpy array
        return None

    def process_video(self, video_id, file_path):
        embeddings = self.extract_video_embeddings(file_path)
        if embeddings is not None:
            print(f"Extracted embeddings for video {video_id}: {embeddings.shape}")
        else:
            print(f"Failed to extract embeddings for video {video_id}")
        return embeddings


if __name__ == "__main__":
    video_path = "path_to_your_video.mp4"
    ## extractor = EmbeddingExtractor(model_name="EfficientNetV2B0")  # Change model name here
    extractor = EmbeddingExtractor(
        model_name="x3d_m"
    )  # You can change to x3d_s or x3d_l
    extractor.process_video(1, video_path)
