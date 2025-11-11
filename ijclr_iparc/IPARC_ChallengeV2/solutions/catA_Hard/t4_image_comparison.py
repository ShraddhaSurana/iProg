"""Module ID: 4
Title: image comparison
Specification: Create a function that will compare two images and return true if they are exactly the same. Create another function that calls this function, but takes as input two columns consisting of images and returns true only if all the images are the same.
Inputs: create your own test cases that will test these two functions
Output: the two functions
"""

import numpy as np

def compare_images(img1, img2):
    """
    Compare two images (2D numpy arrays).
    
    Args:
    img1, img2 (np.array): Two images to be compared.
    
    Returns:
    bool: True if the images are the same, False otherwise.
    """
    return np.array_equal(img1, img2)

def compare_columns(transformed_images, expected_images):
    """
    Compare two columns of images.
    
    Args:
    transformed_images, expected_images (list of np.array): Two columns of images to be compared. 
                                                            Each column is a list of images.
    
    Returns:
    bool: True if all images in the columns are the same, False otherwise.
    """
    for trans_img, exp_img in zip(transformed_images, expected_images):
        if not compare_images(trans_img, exp_img):
            return False
    return True

if __name__ == "__main__":

    # Test cases
    img1 = np.array([[0, 1], [1, 0]])
    img2 = np.array([[0, 1], [1, 0]])
    img3 = np.array([[1, 0], [0, 1]])

    print(compare_images(img1, img2))  # True
    print(compare_images(img1, img3))  # False

    transformed_images_1 = [img1, img2]
    expected_images_1 = [img1, img2]
    transformed_images_2 = [img1, img2]
    expected_images_2 = [img2, img3]

    print(compare_columns(transformed_images_1, expected_images_1))  # True
    print(compare_columns(transformed_images_2, expected_images_2))  # False