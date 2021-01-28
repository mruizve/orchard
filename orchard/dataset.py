import numpy as np
import os
import sys
import cv2

import mrcnn.utils


class OrchardDataset(mrcnn.utils.Dataset):
    def load(self, dataset_path, fruit, subset):
        # dataset structure:
        # + root
        # |-+ fruit
        # | |-+ annotations
        # | | '- CSV files with same name as the ones in the images
        # | |    format: item [number], c-x [pixels], c-y [pixels], radius [pixels], label [always 1]
        # | |-+ images
        # | | '- PNG images.
        # | |-+ segmentations
        # | | '- PNG images with same name as the ones in the images folder but with a _L suffix.
        # | '-+ sets
        # .   '- {all, test, train, train_val, val}.txt

        # Validate dataset path
        if not os.path.exists(dataset_path):
            raise RuntimeError('{} is not a valid directory'.format(dataset_path))
        fruit_paths = [entry.path for entry in os.scandir(dataset_path) if entry.is_dir()]
        if not fruit_paths:
            raise RuntimeError('{} is not a valid dataset path: no fruits found'.format(dataset_path))
        fruit_names = list(map(lambda x: x[x.rfind(os.sep)+1:], fruit_paths))

        # Validate fruit type
        if fruit not in fruit_names:
            raise RuntimeError('unknown fruit {}. available fruits are: {}'.format(fruit, fruit_names))

        # Validate subset
        subset_paths = [entry.path for entry in os.scandir(os.path.join(dataset_path, fruit, 'sets')) if entry.is_file()]
        if not subset_paths:
            raise RuntimeError('{} is not a valid dataset path: no subsets found for fruit {}'.format(dataset_path, fruit))
        subset_names = list(map(lambda x: os.path.splitext(x[x.rfind(os.sep)+1:])[0], subset_paths))
        if subset not in subset_names:
            raise RuntimeError('unknown subset {}. available subsets for fruit {} are: {}'.format(subset, fruit, subset_names))

        # Set the instance source
        self.source = 'orchard'

        # Add classes. We have only one class to add.
        self.add_class(self.source, 1, fruit)

        with open(subset_paths[subset_names.index(subset)], 'rt') as subset_file:
            line = subset_file.readline()
            while line:
                image_id = line.strip()

                # Validate sample data
                image_path = os.path.join(dataset_path, fruit, 'images', image_id + '.png')
                annotations_path = os.path.join(dataset_path, fruit, 'annotations', image_id + '.csv')
                mask_path = os.path.join(dataset_path, fruit, 'segmentations', image_id + '_L.png')
                if not os.path.exists(image_path) or not os.path.exists(annotations_path) or not os.path.exists(mask_path):
                    print('WARNING: skipping image {}: some sample data is missing'.format(image_path), file=sys.stderr)
                    line = subset_file.readline()
                    continue

                # Load annotations
                annotations = []
                with open(annotations_path, 'rt') as annotations_file:
                    line = annotations_file.readline()
                    while line:
                        if line[0] != '#':
                            annotations.append(list(map(float, line.strip().split(','))))
                        line = annotations_file.readline()
                    annotations = np.array(annotations, dtype=np.float32)
                if annotations.size == 0:
                    line = subset_file.readline()
                    print('INFO: skipping image {}: no annotations to process'.format(image_path), file=sys.stderr)
                    continue

                # Add image
                image_shape = cv2.imread(image_path).shape
                self.add_image(
                    self.source,
                    image_id=image_id,
                    width=image_shape[1],
                    height=image_shape[0],
                    path=image_path,
                    mask_path=mask_path,
                    annotations=annotations)

                line = subset_file.readline()

    def load_mask(self, image_id):
        # Delegate images not belonging to the orchard dataset
        image_info = self.image_info[image_id]
        if image_info['source'] != self.source:
            return super(self.__class__, self).load_mask(image_id)

        # Load sample data (annotations + segmentation mask)
        annotations = image_info['annotations']
        segmentation = cv2.imread(image_info['mask_path'], cv2.IMREAD_GRAYSCALE).astype(np.bool)

        # Generate mask tensor
        height, width = segmentation.shape
        mask = np.zeros((height, width, annotations.shape[0]), dtype=np.bool)
        for i in range(len(annotations)):
            mask_image = np.zeros((height, width), dtype=np.float32)
            cv2.circle(mask_image, (annotations[i, 1], annotations[i, 2]), int(annotations[i, 3]), 255, thickness=cv2.FILLED);
            mask[:,:,i] = np.logical_and(mask_image > 0, segmentation)

        # Return mask, and array of class IDs of each instance.
        # Since we have one class ID only, we return an array of 1s
        return mask, np.ones([mask.shape[-1]], dtype=np.int32)

    def image_reference(self, image_id):
        # Delegate images not belonging to the orchard dataset
        info = self.image_info[image_id]
        if info["source"] != self.source:
            return super(self.__class__, self).image_reference(image_id)
        return info["path"]
