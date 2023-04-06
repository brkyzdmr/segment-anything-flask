import io
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image

def get_mask_image(mask):
    color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color[:3].reshape(1, 1, -1)
    mask_image = (mask_image * 255).astype(np.uint8)
    return Image.fromarray(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))   
    
def read_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return image

def combine_images(original_image, mask_image):
    original_array = np.array(original_image)
    mask_array = np.array(mask_image)

    mask_array = mask_array.astype(np.float32)

    # resize mask to match aspect ratio of original image
    orig_height, orig_width, _ = original_array.shape
    mask_array = cv2.resize(mask_array, (orig_width, orig_height))

    mask_array = np.squeeze(mask_array)

    print("mask_array.shape: ", mask_array.shape)
    print("original_array.shape: ", original_array.shape)
    # combine mask and original image apply mask_array color and gray original array where mask_array is not 0, 
    combined_array = np.where(mask_array != 0, mask_array * 0.6 + original_array * 0.4, original_array)
    
    combined_image = Image.fromarray(combined_array.astype(np.uint8))

    return combined_image

def show_image(image, masks = None):
    image = Image.fromarray(image)
    
    if masks is not None:
        mask_image = get_mask_image(masks)
        combined_image = combine_images(image, mask_image)

        img_buffer = io.BytesIO()
        combined_image.save(img_buffer, format='PNG')
    else:
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        
    img_buffer.seek(0)
    img_data = img_buffer.read()
    img_buffer.close()
    
    return img_data

