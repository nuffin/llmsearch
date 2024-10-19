import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.applications import EfficientNetV2B0  # Placeholder for X3D


class EmbeddingExtractor:
    def __init__(self):
        self.model = self.load_3d_model()

    def load_3d_model(self):
        # Load pre-trained EfficientNetV2B0 model for feature extraction (can replace with X3D)
        base_model = EfficientNetV2B0(include_top=False, pooling="avg")
        return tf.keras.Model(inputs=base_model.input, outputs=base_model.output)

    def preprocess_video_frames(self, frames):
        frames = [cv2.resize(frame, (224, 224)) for frame in frames]
        frames = np.array(frames).astype("float32") / 255.0  # Normalize to [0, 1]
        return frames

    def extract_video_embeddings(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
        success = True
        frame_count = 0

        while success and frame_count < 90:  # Extract 90 frames
            success, frame = cap.read()
            if success:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frame_count += 1

        cap.release()

        if len(frames) > 0:
            frames = self.preprocess_video_frames(frames)
            embeddings = self.model.predict(
                np.expand_dims(frames, axis=0)
            )  # Add batch dimension
            return embeddings.squeeze()  # Return embedding as numpy array
        return None

    def process_video(self, video_path, video_id):
        embeddings = self.extract_video_embeddings(video_path)
        if embeddings is not None:
            print(f"Extracted embeddings for video {video_id}: {embeddings.shape}")
        else:
            print(f"Failed to extract embeddings for video {video_id}")
        return embeddings


if __name__ == "__main__":
    video_path = "path_to_your_video.mp4"
    extractor = EmbeddingExtractor()
    extractor.process_video(video_path, video_id=1)
