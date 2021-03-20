# Fruit detection in orchards

Fruit detection on the [ACFR Orchard Fruit Dataset](https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit) using [Mask R-CNN for Object Detection and Segmentation](https://github.com/matterport/Mask_RCNN).

## Requirements
#### Hardware
1. Nvidia GPU with with compute capability between 3.x and 7.5 with at least 8GB of dedicated memory.

#### Software
1. NVidia driver compatible with CUDA 10.x.
2. Recent Docker version.
3. Nvidia container toolkit.

#### Development host
The demo was developed and tested on a notebook with the following specifications:
1. Processor: Intel(R) Core(TM) i9-8950HK CPU @ 2.90GHz.
2. RAM: 32GB DDR4 2667.
3. GPU: GeForce RTX 2070 Mobile.
4. Nvidia driver version 440.64 (CUDA 10.2 capable).
5. Docker version 20.10.1, build 831ebeae96.
6. Nvidia container toolkit version 1.3.0.

## Setting up the container
The first step consist of cloning this repository.
```
git clone https://github.com/mruizve/orchard.git
```

Before getting into the demo it is required to pull or build the Docker image.

To pull the image form DockerHub is enough to execute the following command:
```
docker pull mruizve/orchard
```

Instead, for build it locally it is required to add a copy of the DEB package of the cuDNN runtime library as described [here](https://github.com/mruizve/orchard/blob/main/cudnn/README.md). Then, from the root directory of the repository the image can be built as follows:
```
source scripts/setup.sh
orchard_build
```

Now, in case the image has been pulled from the hub please source the `scripts/setup.sh` file as described above, then start the container:
```
orchard_start
```

## Executing the demo
There are two different choices.

#### Executing the python scripts
The first, to get inside the container and to call directly the training or testing modules of the orchard package. To get inside the container execute the following command
```
orchard_enter
```
Then, for running the demo (i.e., testing the pre-trained model of the apples dataset) inside the container execute:
```
python3 -m orchard.testing --testing-weights ~/weights/mask_rcnn_orchard.h5 apples
```
It is also possible to training a custom model, e.g.,
```
python3 -m orchard.training apples
```
However, it is worth noticing that a proper training session requires tuning some configuration parameters which is not supported by this demo interface. Please consider using the notebooks or cloning the repo inside the container for a proper training session.

#### Running the notebooks
The second alternative for running the demo is to start Jupyter inside the container and to execute the notebooks available at the `samples` directory:
```
orchard_jupyter
```
This will output a message similar to this one:
```
    To access the notebook, open this file in a browser:
        file:///home/demo/.local/share/jupyter/runtime/nbserver-283-open.html
    Or copy and paste one of these URLs:
        http://orchard-demo-container:8888/?token=476671aece297c2c52eb92d04fc0d9a0e5fa349e1bbd68dc
     or http://127.0.0.1:8888/?token=476671aece297c2c52eb92d04fc0d9a0e5fa349e1bbd68dc
```
Copy the last address and paste it inside your browser.

## Links and references
1. [Mask R-CNN for Object Detection and Segmentation](https://github.com/matterport/Mask_RCNN).
2. [Mask R-CNN Ballon tutorial](https://engineering.matterport.com/splash-of-color-instance-segmentation-with-mask-r-cnn-and-tensorflow-7c761e238b46) ([code](https://github.com/matterport/Mask_RCNN/tree/master/samples/balloon)).
3. [Applications of AI and Computer Vision in Agriculture-Fruit recognition, localization and segmentation](https://github.com/mjjackey/Mask_R_CNN_in_Fruit_Counting) (not so useful).
4. [Tenfsorflow compatibility with CUDA](https://www.tensorflow.org/install/source#gpu).
5. [Tenfsorflow compatibility with Keras](https://docs.floydhub.com/guides/environments/).
6. [ACFR Orchard Fruit Dataset](https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit). Direct download [link](https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/acfr-multifruit-2016.zip).
7. [QUT-HIA-DAF and BUP Capsicum Datasets](https://data.researchdatafinder.qut.edu.au/dataset/qut-hia-daf-capsicum-datasets). Direct download links: [QHD Polytunel](https://data.researchdatafinder.qut.edu.au/dataset/fc42f962-29c8-4be4-8d29-f61ebe165264/resource/b168423a-8b77-4649-be9f-921f196ea608/download/qhdp2020.tar.gz), [QHD Field](https://data.researchdatafinder.qut.edu.au/dataset/fc42f962-29c8-4be4-8d29-f61ebe165264/resource/1fdca442-dca0-4fd0-8412-4231297336a9/download/qhdf2020.tar.gz), [BUP Protected cropping](https://data.researchdatafinder.qut.edu.au/dataset/fc42f962-29c8-4be4-8d29-f61ebe165264/resource/54d434de-30c0-4e01-947b-68c2ff37ae58/download/bup2020.tar.gz).
8. [Practical Deep Learning in Life - Plant Pathology 2020](https://manycoding.github.io/fastpages/2020/05/29/Practical-Deep-Learning-in-Life-Plants.html).
9. [Tensorflow Certification Study Guide](https://github.com/nicholasjhana/tensorflow-certification-study-guide).
