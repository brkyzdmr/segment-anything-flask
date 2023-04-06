from segment_anything import sam_model_registry, SamPredictor
from scripts.utils import read_image, show_image
import onnxruntime
import numpy as np

class SamImagePredictor:
    def __init__(self, checkpoint_path, onnx_model_path, model_type="default"):
        self.checkpoint_path = checkpoint_path
        self.onnx_model_path = onnx_model_path
        self.model_type = model_type
        self.image = None
        self.sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
        self.ort_session = onnxruntime.InferenceSession(onnx_model_path)
        self.sam.to(device='cuda')
        self.predictor = SamPredictor(self.sam)

    def set_image(self, image_path):
        self.image = read_image(image_path)
        self.predictor.set_image(self.image)
        self.image_embedding = self.predictor.get_image_embedding().cpu().numpy()

    def calculate_position(self, x, y):
        input_point = np.array([[x, y]])
        input_label = np.array([1])
        onnx_coord = np.concatenate([input_point, np.array([[0.0, 0.0]])], axis=0)[None, :, :]
        onnx_label = np.concatenate([input_label, np.array([-1])], axis=0)[None, :].astype(np.float32)

        onnx_coord = self.predictor.transform.apply_coords(onnx_coord, self.image.shape[:2]).astype(np.float32)
        onnx_mask_input = np.zeros((1, 1, 256, 256), dtype=np.float32)
        onnx_has_mask_input = np.zeros(1, dtype=np.float32)

        ort_inputs = {
            "image_embeddings": self.image_embedding,
            "point_coords": onnx_coord,
            "point_labels": onnx_label,
            "mask_input": onnx_mask_input,
            "has_mask_input": onnx_has_mask_input,
            "orig_im_size": np.array(self.image.shape[:2], dtype=np.float32)
        }

        masks, _, low_res_logits = self.ort_session.run(None, ort_inputs)
        masks = masks > self.predictor.model.mask_threshold

        img_data = show_image(self.image, masks)
        return img_data
