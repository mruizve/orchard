#!/usr/bin/env python3
import argparse
import matplotlib
matplotlib.use('TkAgg')

import mrcnn.config
import mrcnn.model
import mrcnn.visualize
import orchard.dataset
import orchard.config
import orchard.utils


def testing(dataset, weights_path):
    inference_config = orchard.config.InferenceConfig()
    #inference_config.display()

    # Create the model in inference mode and load weights
    model = mrcnn.model.MaskRCNN(
        mode='inference',
        config=inference_config,
        model_dir=inference_config.LOGS_PATH)
    orchard.utils.load_weights(model, weights_path)

    # Test on all images
    for image_id in dataset.image_ids:
        image, _, gt_class_id, gt_bbox, gt_mask = mrcnn.model.load_image_gt(
            dataset,
            inference_config,
            image_id,
            use_mini_mask=False)

        results = model.detect([image])
        r = results[0]

        mrcnn.visualize.display_differences(
            image,
            gt_bbox, gt_class_id, gt_mask,
            r['rois'], r['class_ids'], r['scores'], r['masks'],
            dataset.class_names)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='training script of the orchard package')
    parser.add_argument('fruit', help='target fruit')
    parser.add_argument('--testing-weights', default='orchard', help='path to the model weights')
    options = parser.parse_args()

    # Testing dataset
    dataset_test = orchard.dataset.OrchardDataset()
    dataset_test.load(orchard.config.OrchardConfig.DATASET_PATH, options.fruit, 'test')
    dataset_test.prepare()

    testing(dataset_test, options.testing_weights)
