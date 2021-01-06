#!/usr/bin/env python3
import argparse
import numpy as np

import mrcnn.utils
import mrcnn.model
import orchard.dataset
import orchard.config
import orchard.utils


def training(dataset_train, dataset_val, weights_path):
    config = orchard.config.TrainingConfig()
    #config.display()

    # Create model in training mode and load weights
    model = mrcnn.model.MaskRCNN(
        mode='training',
        config=config,
        model_dir=config.LOGS_PATH)
    orchard.utils.load_weights(model, weights_path)

    # Train the head branches
    # Only the heads. Here we're freezing all the backbone layers and training only the randomly initialized layers
    # (i.e. the ones that we didn't use pre-trained weights from MS COCO).
    # To train only the head layers, pass `layers='heads'` to the `train()` to freezes all layers except the head layers.
    # You can also pass a regular expression to select which layers to train by name pattern.
    model.train(
        dataset_train, dataset_val,
        learning_rate=config.LEARNING_RATE,
        epochs=config.EPOCHS_HEAD,
        layers='heads')

    # Fine tune all layers
    # Simply pass `layers="all` to train all layers. It is also possible to pass a regular expression to select which
    # layers to train by name pattern.
    model.train(
        dataset_train, dataset_val,
        learning_rate=config.LEARNING_RATE / 10,
        epochs=config.EPOCHS_ALL,
        layers="all")

    # Save weights
    # Typically not needed because callbacks save after every epoch
    # Uncomment to save manually
    # weights_path = os.path.join(MODEL_DIR, "mask_rcnn_shapes.h5")
    # model.keras_model.save_weights(weights_path)


def validation(datasets, weights_path):
    inference_config = orchard.config.InferenceConfig()
    #inference_config.display()

    # Create the model in inference mode and load weights
    model = mrcnn.model.MaskRCNN(
        mode='inference',
        config=inference_config,
        model_dir=inference_config.LOGS_PATH)
    orchard.utils.load_weights(model, weights_path)

    # Compute VOC-Style mAP @ IoU=0.5
    # Running on 100 images. Increase for better accuracy.
    for dataset in datasets:
        APs = []
        for image_id in dataset.image_ids:
            # Load image and ground truth data
            image, image_meta, gt_class_id, gt_bbox, gt_mask = mrcnn.model.load_image_gt(
                dataset,
                inference_config,
                image_id,
                use_mini_mask=False)

            molded_images = np.expand_dims(mrcnn.model.mold_image(image, inference_config), 0)

            # Run object detection
            results = model.detect([image], verbose=0)

            r = results[0]

            # Compute AP
            AP, precisions, recalls, overlaps = mrcnn.utils.compute_ap(
                gt_bbox,
                gt_class_id,
                gt_mask,
                r['rois'], r['class_ids'], r['scores'], r['masks'])
            APs.append(AP)
        print('mAP: {}'.format(np.mean(APs)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='training script of the orchard package')
    parser.add_argument('fruit', help='target fruit')
    parser.add_argument('--skip-training', action='store_true', help='set to skip the training phase')
    parser.add_argument('--skip-validation', action='store_true', help='set to skip the validation phase')
    parser.add_argument('--training-weights', default='coco', help='path to the model weights')
    parser.add_argument('--validation-weights', default='last', help='path to the model weights')
    options = parser.parse_args()

    if not options.skip_training:
        # Training dataset
        dataset_train = orchard.dataset.OrchardDataset()
        dataset_train.load(orchard.config.OrchardConfig.DATASET_PATH, options.fruit, 'train')
        dataset_train.prepare()

    if not options.skip_training or not options.skip_validation:
        # Validation dataset
        dataset_val = orchard.dataset.OrchardDataset()
        dataset_val.load(orchard.config.OrchardConfig.DATASET_PATH, options.fruit, 'val')
        dataset_val.prepare()

    if not options.skip_validation:
        # Testing dataset
        dataset_test = orchard.dataset.OrchardDataset()
        dataset_test.load(orchard.config.OrchardConfig.DATASET_PATH, options.fruit, 'test')
        dataset_test.prepare()

    # Training and validation
    if not options.skip_training:
        training(dataset_train, dataset_val, options.training_weights)
    if not options.skip_validation:
        validation([dataset_val, dataset_test], options.validation_weights)
