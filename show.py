"""
==============================================================
script to show the image and label, or image with labeled mask
==============================================================

Author: Muhammad Faizan
Date: 13 May 2023
Copywrite (c) Muhammad Faizan
==============================================================
"""
import matplotlib.pyplot as plt
import logging
import argparse
import numpy as np
import hydra
from omegaconf import DictConfig
import sys
import nibabel as nib

import torch
from brats import get_datasets
from utils.visualizer import visualize_abnormal_area, get_labelled_image, visualize_data_gif
from utils.general import visualize_data_sample

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s: %(name)s: %(message)s")
file_handler = logging.FileHandler(filename= "logger/show.log")
stream_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def load_patient_case(path, type = "T1", slice = 75, load_label = True):
    
    # load nifti image
    file = nib.load(path)
    image = file.get_fdata()
    print(image.shape)





@hydra.main(config_name='configs', config_path= 'conf', version_base=None)
def show_result(cfg: DictConfig, args:argparse.Namespace):
    """
    Visualize labelled brain scan on a patient case, three options are available
    1 - create brain scan slices and label them
    2 - create a .gif format file to visualize part of brain (labelled)
    3 - visualize a scan with it's label in a subplot format
    """
   
    # Load data
    dataset = get_datasets(cfg.dataset.dataset_folder, "test")
    data_loader = torch.utils.data.DataLoader(dataset, 
                                            batch_size=1, 
                                            shuffle=False, num_workers=8, 
                                            pin_memory=True) 
    
    # batch of data
    batch = next(iter(data_loader))
    image, label = batch["image"], batch['label']
    logger.info('visualizing an image with label')

    # Visualize 
    if args.get_abnormal_area:
        visualize_abnormal_area(image, label)
    elif args.visualize_data_gif:
        labelled_img = get_labelled_image(image, label)
        visualize_data_gif(labelled_img)
    elif args.visualize_data_sample:
        visualize_data_sample(args.test_patient_path, 
                              cfg.paths.test_patient)
    else:
        logger.info('No option selected')
        sys.exit()


if __name__ == "__main__":
    # Visualize
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["show-abnormal-image", "get-gif", "show-case"], default="get-gif", 
                        help="visulization options")
    parser.add_argument("--scan_path", default= "", type = str, 
                        help = "path to patient MRI scan")
    parser.add_argument("--modality", default= "T1", type = str, 
                        help = "type of modality type for analysis and visualization")
    
    args = parser.parse_args()
    # show_result(args)
    load_patient_case(path=args.scan_path, type=args.modality, slice=75, load_label=True)
    print('Done!!!')