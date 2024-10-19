import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.applications import EfficientNetV2B0
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input


class EmbeddingExtractor:
    def __init__(self):
        self.model = self.load_efficientnet_model()

    def load_efficientnet_model(self):
        # Load pre-trained EfficientNetV2B0 model for feature extraction
        base_model = EfficientNetV2B0(include_top=False, pooling="avg")
        return tf.keras.Model(inputs=base_model.input, outputs=base_model.output)

    def preprocess_image(self, image):
        image = cv2.resize(image, (224, 224))
        image = image.astype("float32")
        image = preprocess_input(
            image
        )  # Preprocess with EfficientNetV2 specific preprocessing
        return image

    def extract_image_embedding(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = self.preprocess_image(image)
            embedding = self.model.predict(
                np.expand_dims(image, axis=0)
            )  # Add batch dimension
            return embedding.squeeze()  # Return embedding as numpy array
        return None

    def process_image(self, image_path, image_id):
        embedding = self.extract_image_embedding(image_path)
        if embedding is not None:
            print(f"Extracted embedding for image {image_id}: {embedding.shape}")
        else:
            print(f"Failed to extract embedding for image {image_id}")
        return embedding


if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"
    extractor = EmbeddingExtractor()
    extractor.process_image(image_path, image_id=1)
