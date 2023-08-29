from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

class ProcessedImage:
    def __init__(self, image_path:str):
        self.image_path = image_path
        self.model = hub.load('https://tfhub.dev/tensorflow/faster_rcnn/inception_resnet_v2_1024x1024/1')
        self.PATH_TO_LABELS = 'models/research/object_detection/data/mscoco_label_map.pbtxt'
        self.category_index = label_map_util.create_category_index_from_labelmap(self.PATH_TO_LABELS, use_display_name=True)

    def load_image(self) -> tuple:
        image = cv2.imread(self.image_path)
        return image, None

    def convert_to_hsv(self, tuple) -> tuple:
        image, _ = tuple
        return image, cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    def get_red_mask(self, tuple) -> tuple:
        image, hsv = tuple
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        return image, cv2.inRange(hsv, lower_red, upper_red)

    def apply_blur(self, tuple) -> tuple:
        image, mask = tuple
        return image, cv2.GaussianBlur(mask,(5,5),0)

    def find_contours(self, tuple) -> tuple:
        image, blur = tuple
        contours, _ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return image, contours

    def model_processing(self, tuple):
        image, _ = tuple
        # Convert the image to RGB and add a batch dimension
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb_tensor = tf.expand_dims(rgb, axis=0)
        # Run the model
        outputs = self.model(rgb_tensor)
        # Prepare a list for the model's bounding boxes, classes, and scores
        self.model_boxes = outputs['detection_boxes'][0].numpy()
        self.model_classes = (outputs['detection_classes'][0].numpy() + 1).astype(int)
        self.model_scores = outputs['detection_scores'][0].numpy()
        return image, (self.model_boxes, self.model_classes, self.model_scores)

    def draw_model_boxes(self, tuple):
        image, (model_boxes, model_classes, model_scores) = tuple
        # Convert the image to RGB for visualization
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Draw the labels on the image
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_rgb,
            model_boxes,
            model_classes,
            model_scores,
            self.category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.30,
            agnostic_mode=False,
        )
        # Convert the image back to BGR for further processing
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        return image_bgr, None

    def draw_color_boxes(self, tuple):
        image, contours = tuple
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return image

    def main(self):
    # Create the pipeline
        pipeline = Pipeline([
            ('load_image', FunctionTransformer(self.load_image, validate=False)),
            ('convert_to_hsv', FunctionTransformer(self.convert_to_hsv, validate=False)),
            ('get_red_mask', FunctionTransformer(self.get_red_mask, validate=False)),
            ('apply_blur', FunctionTransformer(self.apply_blur, validate=False)),
            ('find_contours', FunctionTransformer(self.find_contours, validate=False)),
            ('model_processing', FunctionTransformer(self.model_processing, validate=False)),
            ('draw_model_boxes', FunctionTransformer(self.draw_model_boxes, validate=False)),
            ('draw_color_boxes', FunctionTransformer(self.draw_color_boxes, validate=False)),
        ])
        processed_image_result = pipeline.transform(self.image_path)

        # Display the processed image
        cv2.imshow('image', processed_image_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
if __name__ == "__main__":
    processed_image = ProcessedImage(image_path = "tiger.jpg")
    processed_image.main()
