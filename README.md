# Flask Application of Meta's Segment Anything Model

This is a Flask application that implements Meta's Segment Anything Model for segmenting images by mouse click in real-time performance. There are 3 images in the project, they will sequentially load, and you will interact with them by mouse click.

## Requirements
To install the necessary Python packages, run the following command:

```shell
pip install -r requirements.txt
```
If you want to use your CUDA cores, you can download the necessary toolkit with the following command (default is CPU):
```shell
conda install -c anaconda cudatoolkit=11.8
```

## Installing Models 
[ViT-H SAM model (default) - 2.4 GB]("https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth")
[ViT-L SAM model - 1.2 GB]("https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth")
[ViT-B SAM model - 358 MB]("https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth")

## Configuration
There is a file called [config.yaml](/config.yaml), where you can set your configs.

```yaml
checkpoint: 'models\sam_vit_h_4b8939.pth'
onnx_model: 'models\sam_onnx_quantized_example.onnx'
images_folder: 'static\images'
model_type: 'default'
```

## Running the Application
By default, the application runs in Onnx runtime, which provides real-time execution performance. To run the application, execute the following command:

```shell
flask --app app.py run
```

## Examples
![People](/examples/1.png "People")

![Istanbul](/examples/2.png "Istanbul")

![Book Shelf](/examples/3.png "Book Shelf")