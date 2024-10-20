import tensorflow as tf
import cv2
import numpy as np
from transformers import TFAutoModel, AutoConfig
from tensorflow.keras.applications import (
    EfficientNetV2B0,
    ResNet50,
    preprocess_input as keras_preprocess_input,
)


# EmbeddingExtractor Class with model name as a parameter
class EmbeddingExtractor:
    def __init__(self, model_name="EfficientNetV2B0"):
        self.model_name = model_name
        self.model, self.preprocess_fn = self.load_model()

    def load_model(self):
        if self.model_name == "EfficientNetV2B0":
            base_model = EfficientNetV2B0(include_top=False, pooling="avg")
            preprocess_fn = (
                keras_preprocess_input  # Define custom preprocessing if needed
            )
        elif self.model_name == "ResNet50":
            base_model = ResNet50(include_top=False, pooling="avg")
            preprocess_fn = (
                keras_preprocess_input  # Define custom preprocessing if needed
            )
        else:
            config = AutoConfig.from_pretrained(self.model_name)
            base_model = TFAutoModel.from_pretrained(self.model_name, config=config)
            preprocess_fn = (
                keras_preprocess_input  # Define custom preprocessing if needed
            )

        return (
            tf.keras.Model(inputs=base_model.input, outputs=base_model.output),
            preprocess_fn,
        )

    def preprocess_image(self, image):
        image = cv2.resize(image, (224, 224))
        image = image.astype("float32")
        image = self.preprocess_fn(image)
        return image

    def extract_image_embedding(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = self.preprocess_image(image)
            embedding = self.model.predict(np.expand_dims(image, axis=0))
            return embedding.squeeze()
        return None

    def process_image(self, image_id, file_path):
        embedding = self.extract_image_embedding(file_path)
        if embedding is not None:
            print(f"Extracted embedding for image {image_id}: {embedding.shape}")
        else:
            print(f"Failed to extract embedding for image {image_id}")
        return embedding


if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"

    # Pass the model name as a parameter
    model_name = "microsoft/resnet-50"  # Example for Hugging Face model
    extractor = EmbeddingExtractor(model_name=model_name)

    # Process the image
    extractor.process_image(1, image_path)
