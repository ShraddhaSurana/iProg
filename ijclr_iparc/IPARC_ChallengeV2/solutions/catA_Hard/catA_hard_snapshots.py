import json
import numpy as np
import pandas as pd
import os
import time
import re
from itertools import product
from t1_load_data import load_data
from t1_load_multiband_data import load_multiband_data
from t2_define_SEs import get_structuring_elements
from t5_apply_transformation import apply_transformations_to_all
from t6_generate_sequence import find_candidate_sequences
from t4_image_comparison import compare_columns


def find_sequence_for_band(img_band_input, img_band_output, sequence_length, SE_dict):
    '''
    Function to find the successful sequence of operations that transforms the input images to the output images for a specific band.
    Args:
    img_band_input, img_band_output: list[2D np.array]
        Input and output images for the band.
    sequence_length: int
        Maximum length of the sequence of operations.
    SE_dict: dict
        Dictionary of structuring elements.
    Returns:
    sequence_list: list of tuples
        List of successful sequence of operations for the band (may be empty if no sequence is found).
    '''
    count = 0
    sequence_list = []
    # Generate all possible sequences of operations of given length
    sequence_candidates = find_candidate_sequences(sequence_length, SE_dict)
    # op_count=0
    # For each candidate sequence
    for operations in sequence_candidates:
        # op_count = op_count + 1
        # Apply the operation sequence to all input images
        transformed_images = apply_transformations_to_all(img_band_input, operations, SE_dict)
        # Check if the transformed images match the output images
        if compare_columns(transformed_images, img_band_output):
            # If sequence is successful, store it
            sequence_list.append(operations)
            count += 1
    print(f"Number of candidate sequences: {count}")
    return sequence_list


def get_expected_images(snapshot_df):
    """
    Convert snapshot DataFrame into numpy arrays for each band.

    Parameters:
    snapshot_df (pd.DataFrame): A DataFrame with columns 'band_1', 'band_2', and 'band_3',
                                each containing a list of lists (2D image).

    Returns:
    List[np.ndarray]: A list of numpy arrays with shape (H, W, 3) representing expected RGB-style band images.
    """
    expected_images = []

    for _, row in snapshot_df.iterrows():
        band_1 = np.array(row['band_1'], dtype=np.uint8)
        band_2 = np.array(row['band_2'], dtype=np.uint8)
        band_3 = np.array(row['band_3'], dtype=np.uint8)
        expected_images.append({'band_1': band_1, 'band_2': band_2, 'band_3': band_3})

    return expected_images


def get_candidate_sequences_for_each_band(file_path, sequence_length, print_seq=False):
    """
        Given the filepath to JSON file containing image data, get the candidate sequences for each band.
        Args:
        filepath (str): The file path of JSON containing image data
        sequence_length (int): Maximum length of the sequence of operations.
        Returns:
        dictionary: A dictionary containing three list. Each inner list represents the sequence of
                      operations for each band.
        """
    sequence_dict = {}
    snapshot_path = file_path.rsplit(".json", 1)[0] + "_snapshot.json"
    snapshot_data = load_data(snapshot_path)
    expected_images = get_expected_images(snapshot_data)

    # Load the multiband image data
    df = load_multiband_data(file_path)
    # Get the structuring elements
    SE_dict = get_structuring_elements()
    # For each band
    for band in range(3):
        # Get the input image bands
        img_band_input = [img[band] for img in df['input'].values]
        # Get the output image bands
        expected_image_band = [img[f'band_{band+1}'] for img in expected_images]
        # Find the successful sequence of operations for the band
        sequence_list = find_sequence_for_band(img_band_input, expected_image_band, sequence_length, SE_dict)
        if sequence_list:
            sequence_dict[band+1] = sequence_list
            if print_seq:
                print(f"Successful sequences of operations for band {band+1} are {sequence_list}")
    return sequence_dict
def generate_all_combinations_of_colour_rule():
    """
    Function to generate a list of all unique combinations of colour rules.
    Returns:
    list of colour rules: each rule is a list of 8 elements, where each element
                         is also a list in the form [b1, b2, b3, c] where b1, b2, b3 are
                         the three-bit binary sequence and c is the colour code.
    """
    binary_seq = [[0, 0, 1], [0, 1, 0], [0, 1, 1],
                  [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
    color_combinations = list(product([1, 2, 3], repeat=7))
    all_rules = []
    for combination in color_combinations:
        rule = [[0, 0, 0, 0]] + [binary_seq[i] + [c] for i, c in enumerate(combination)]
        all_rules.append(rule)
    return all_rules
def combine_bands_with_color_rule_list_optimized(image_band1_list, image_band2_list, image_band3_list, color_rule):
    """
    Function to combine three image bands using a specific color rule.
    :param image_band1_list: List of images representing band 1
    :param image_band2_list: List of images representing band 2
    :param image_band3_list: List of images representing band 3
    :param color_rule: A color rule used to convert binary bands into one image
    :return: A list of combined images
    """
    h, w = image_band1_list[0].shape  # Assuming all images in the list have the same size
    n_images = len(image_band1_list)  # Assuming the lists for all bands have the same length
    # Create a mapping array with default values from color_rule
    mapping = np.zeros((2, 2, 2), dtype=np.uint8)
    for rule in color_rule:
        mapping[tuple(rule[:3])] = rule[3]
    combined_images_list = []
    for img_number in range(n_images):
        combined_image = np.stack(
            (
                image_band1_list[img_number].astype(np.uint8),
                image_band2_list[img_number].astype(np.uint8),
                image_band3_list[img_number].astype(np.uint8)
            ), -1
        )
        combined_images_list.append(mapping[combined_image[..., 0], combined_image[..., 1], combined_image[..., 2]])
    return combined_images_list

def find_solution(sequence_dict, all_colour_rules, input_band1, input_band2, input_band3, expected_image, SE_dict):
    """
    The revised function will now use the existing apply_transformations_to_all function to apply the transformations to all images and checks for the correct sequence
    that gives the expected image. Iterates over all operations sequence combinations and color rules to exhaustively check all scenarios
    that match the output image.
    """
    for sequence_band1 in sequence_dict[1]:
        image_band1 = apply_transformations_to_all(input_band1, sequence_band1, SE_dict)
        for sequence_band2 in sequence_dict[2]:
            image_band2 = apply_transformations_to_all(input_band2, sequence_band2, SE_dict)
            for sequence_band3 in sequence_dict[3]:
                image_band3 = apply_transformations_to_all(input_band3, sequence_band3, SE_dict)
                for color_rule in all_colour_rules:
                    # merge the bands into one using the color rule
                    output_image = combine_bands_with_color_rule_list_optimized(image_band1, image_band2, image_band3, color_rule)
                    # check if the output image is correct, if not keep trying
                    if np.array_equal(output_image, expected_image):
                        return sequence_band1, sequence_band2, sequence_band3, color_rule
    return None


def transform_to_json_format(result):
    """Transform result to the specified JSON format."""
    output = []

    # Add indexed arrays to output
    for i, sublist in enumerate(result[:-1]):
        for action, element in sublist:
            output.append([i + 1, action, element])

    # Add null index and color rule
    color_rule = result[-1]
    output.append([None, 'color_rule', color_rule])

    # Convert the output to a JSON string
    json_output = json.dumps(output)

    return json_output


def execute_task(task_file):
    print(task_file)
    start_time = time.time()
    sequence_length = 4
    sequence_dict = get_candidate_sequences_for_each_band(task_file, sequence_length, False)
    all_colour_rules = generate_all_combinations_of_colour_rule()
    original_data = load_data(task_file)
    expected_images = [np.array(img) for img in original_data['output']]
    df = load_multiband_data(task_file)
    SE_dict = get_structuring_elements()

    img_band1_input = [img[0] for img in df['input'].values]
    img_band2_input = [img[1] for img in df['input'].values]
    img_band3_input = [img[2] for img in df['input'].values]

    result = find_solution(sequence_dict, all_colour_rules, img_band1_input, img_band2_input,
                           img_band3_input, expected_images, SE_dict)
    end_time = time.time()
    task_id = os.path.splitext(os.path.basename(task_file))[0]
    time_elapsed = end_time - start_time
    result_json = transform_to_json_format(result)

    return {'task_id': task_id, 'solution': result_json, 'time_taken': time_elapsed}

if __name__ == "__main__":
    # When examining one file:
    # file_path = "../../../src/IPARC_ChallengeV2/Dataset/CatA_Hard/Task007.json"
    # task_files = [file_path]
    task_files = ["../../../src/IPARC_ChallengeV2/Dataset/CatA_Hard_snapshot_test/{}".format(f) for f in
                  os.listdir("../../Dataset/CatA_Hard_snapshot_test") if re.search("Task[0-9]{3}\.json", f)]


    results = []
    for task_file in task_files:
        result = execute_task(task_file)
        print(result)
        results.append(result)
    results_df = pd.DataFrame(results, columns=["task_id", "solution", "time_taken"])
    results_df.to_csv("task_results_catA_Hard_with_snapshots_catC_test.csv", index=False)

