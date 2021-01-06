import os

import mrcnn.utils
import orchard.config


def load_weights(model, weights_path):
    config = orchard.config.OrchardConfig()

    if weights_path == 'last':
        # Load last trained weights
        model.load_weights(model.find_last(), by_name=True)

    elif weights_path == 'coco':
        # Download COCO pre-trained weights
        config = orchard.config.OrchardConfig()
        if not os.path.exists(config.COCO_WEIGHTS_PATH):
            if not os.path.exists(config.WEIGHTS_PATH):
                os.makedirs(config.WEIGHTS_PATH)
            mrcnn.utils.download_trained_weights(config.COCO_WEIGHTS_PATH)

        # Load weights trained on MS COCO, but skip layers that
        # are different due to the different number of classes
        model.load_weights(
            config.COCO_WEIGHTS_PATH,
            by_name=True,
            exclude=['mrcnn_class_logits', 'mrcnn_bbox_fc', 'mrcnn_bbox', 'mrcnn_mask'])

    elif weights_path == 'orchard':
        model.load_weights(config.ORCHARD_WEIGHTS_PATH, by_name=True)

    else:
        # Load weights from a custom path
        if not os.path.exists(weights_path):
            raise RuntimeError('cannot load model weights: {} is not a invalid path'.format (weights_path))
        model.load_weights(weights_path, by_name=True)


