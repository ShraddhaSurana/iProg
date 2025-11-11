"""Module ID: 6
Title: generate sequence
Specification: The previous function was applying a sequence of operations with SE. This function is to write a function that creates candidate sequences for a task and calls this function and then verifies it. These are the functions created in the previous module that you will need to use: load_data(filepath): Function to load data from a json file into a pandas DataFrame. Args: filepath (str): Path to the json file. Returns: df (DataFrame): Pandas dataframe containing the data.
Inputs: get_structuring_elements(): Returns the predefined structuring elements as a dictionary. Returns: dict of {str: list[list[int]]}: A dictionary where the keys are the structuring element names and the values are their corresponding 3x3 binary matrices, represented as nested lists.
perform_dilation(image, se, repetitions=1): Apply the dilation operation to a binary image for a given number of times using a given structuring element. Args: image (np.array): Binary image to be transformed.; se (np.array): Structuring element to be used in the dilation operation.; repetitions (int): The number of times to apply the dilation operation. Default is 1. Returns: (np.array): The transformed binary image after dilation.
perform_erosion(image, se, repetitions=1): Apply the erosion operation to a binary image for a given number of times using a given structuring element. Args: image (np.array): Binary image to be transformed.; se (np.array): Structuring element to be used in the erosion operation.; repetitions (int): The number of times to apply the erosion operation. Default is 1. Returns: (np.array): The transformed binary image after erosion.
compare_columns(transformed_images, expected_images): Compare two columns of images. Args: transformed_images, expected_images (list of np.array): Two columns of images to be compared. Each column is a list of images. Returns: bool: True if all images in the columns are the same, False otherwise.
apply_transformations_to_all(images, operations_SE, SE_dict): Apply a sequence of operations (with corresponding SEs) on a list of images Args: images (list[np.array]): The list of images to transform operations_SE (list[tuple]): List of operations with corresponding structuring elements. The tuple format is ('Dilation' or 'Erosion', SE) Returns: list[np.array]: List of transformed images
Output: A function that generates a sequence and calls the existing functions to apply the transformations and verify the correctness.
"""

import itertools

def find_candidate_sequences(n, ses):
    """
    Generate candidate sequences of operations for the morphological transformations.
    It ensures dilations are followed by erosions in the same order as per user specification.
    It also allows repeating operations and SEs in the sequences.
    
    Args:
    n (int): Maximum length of the sequence to generate.
    ses (list[str]): List of all available SEs.
    
    Returns:
    list[tuple]: A list of all candidate sequences of operations up to length n.
    """
    operations = ['Dilation']
    candidate_sequences = []
    
    for length in range(4, n+1):
        for se_sequence in itertools.product(ses, repeat=length):
            dilation_sequence = list(zip(operations*length, se_sequence))
            erosion_sequence = [('Erosion', se) for se in se_sequence]
            combined_sequence = dilation_sequence + erosion_sequence
            candidate_sequences.append(combined_sequence)
                
    return candidate_sequences


def find_candidate_sequences2(n, ses):
    """
    Generate candidate sequences of operations for the morphological transformations.

    Args:
    n (int): Maximum length of the sequence to generate.
    ses (list[str]): List of all available SEs.

    Returns:
    list[tuple]: A list of all candidate sequences of operations up to length 2n.
    """
    sequences = []
    operations = ['Dilation', 'Erosion']

    ses_permutations = list(itertools.product(ses, repeat=n))

    for ses_tuple in ses_permutations:
        sequence = []
        for operation in operations:
            for se in ses_tuple:
                sequence.append((operation, se))
        sequences.append(sequence)

    return sequences