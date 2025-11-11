"""Module ID: 5
Title: apply transformation
Specification: Given an image, The SEs (structuring elements) and the sequence of operations, apply the operations on the given image. The sequence of operation are [operation] [SE] where operation is either Dialtion or Erosion and SE is one of the SE from SEs. Return the transformed image. Create another function that calls this one and applies the given transformation to all the images given in a list of images and returns the corresponding transformed image as a list.
Inputs: create your own test cases that will test these two functions
Output: The two functions
"""
import numpy as np

from projects.iparc.catA_hard.t4_image_comparison import compare_columns
from projects.iparc.catA_hard.t3_dilation_and_erosion_functions import perform_dilation, perform_erosion
from projects.iparc.catA_hard.t1_load_multiband_data import load_multiband_data


def apply_transformations(image, operations_SE, SE_dict):
    """
    Apply a sequence of operations (with corresponding SEs) on an image
    Args:
        image (np.array): The image to transform
        operations_SE (list[tuple]): List of operations with corresponding structuring elements.
                                      The tuple format is ('Dilation' or 'Erosion', SE)
    Returns:
        np.array: The image after applying the operations
    """
    # create a map of operation functions for quickly accessing them
    operation_functions = {
        'Dilation': perform_dilation,
        'Erosion': perform_erosion
    }

    # for every operation in the operations, get the operation function and the SE
    for operation, SE_key in operations_SE:
        se = np.array(SE_dict[SE_key])
        function = operation_functions.get(operation)
        if function:
            image = function(image, se)

    return image


def apply_transformations_to_all(images, operations_SE, SE_dict):
    """
    Apply a sequence of operations (with corresponding SEs) on a list of images
    Args:
        images (list[np.array]): The list of images to transform
        operations_SE (list[tuple]): List of operations with corresponding structuring elements.
                                      The tuple format is ('Dilation' or 'Erosion', SE)
    Returns:
        list[np.array]: List of transformed images
    """
    # transform every image using the above function
    return [apply_transformations(image, operations_SE, SE_dict) for image in images]

if __name__ == '__main__':
    SE_dict = {
        'SE1': [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
        'SE2': [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        'SE3': [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        'SE4': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        'SE5': [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
        'SE6': [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
        'SE7': [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
        'SE8': [[0, 0, 0], [0, 0, 0], [1, 1, 1]]
    }

    operations_SE = [('Dilation', 'SE8'), ('Dilation', 'SE4'), ('Dilation', 'SE6'), ('Dilation', 'SE7'), ('Erosion', 'SE8'),
                     ('Erosion', 'SE4'), ('Erosion', 'SE6'), ('Erosion', 'SE7')]

    # creating a list of two binary images
    # input_images = [np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
    #                 np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])]
    data = load_multiband_data("../../../src/IPARC_ChallengeV2/Dataset/CatA_Hard/Task000.json")
    input_images = data['input']
    transformed_images = apply_transformations_to_all(input_images, operations_SE, SE_dict)

    # for img in transformed_images:
    #     print(img)
    #     print("\n")
    a = compare_columns(transformed_images, data['output'])
    print(a)