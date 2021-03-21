import os

import mrcnn.config


class OrchardConfig(mrcnn.config.Config):
    # Max number of final detections
    DETECTION_MAX_INSTANCES = 50

    # Learning rate and momentum
    LEARNING_RATE = 0.001
    LEARNING_MOMENTUM = 0.9

    # Custom training epochs
    EPOCHS_HEAD = 1
    EPOCHS_ALL = 2

    # Custom data paths -- logs
    LOGS_PATH = os.path.join(os.path.expanduser('~'), 'logs')

    # Custom data paths -- datasets
    ORCHARD_DATASET_PATH = os.path.join(os.path.expanduser('~'), 'datasets', 'orchard')
    PATHOLOGY_DATASET_PATH = os.path.join(os.path.expanduser('~'), 'datasets', 'pathology')

    # Custom data paths -- weights
    WEIGHTS_PATH = os.path.join(os.path.expanduser('~'), 'weights')
    COCO_WEIGHTS_PATH = os.path.join(WEIGHTS_PATH, 'mask_rcnn_coco.h5')
    ORCHARD_WEIGHTS_PATH = os.path.join(WEIGHTS_PATH, 'mask_rcnn_orchard.h5')
    PATHOLOGY_WEIGHTS_PATH = os.path.join(WEIGHTS_PATH, 'efficientnetb7_pathology.h5')


class TrainingConfig(OrchardConfig):
    # Give the configuration a recognizable name
    NAME = "orchard"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + fruit

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    # ~ IMAGE_MIN_DIM = 128
    # ~ IMAGE_MAX_DIM = 128

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8, 16, 32, 64)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 32

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 250

    # Skip detections with < 75% confidence
    DETECTION_MIN_CONFIDENCE = 0.75


class InferenceConfig(TrainingConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
