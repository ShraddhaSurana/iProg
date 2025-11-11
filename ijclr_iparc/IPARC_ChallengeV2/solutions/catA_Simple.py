import pandas as pd
import itertools
import numpy as np
import scipy.signal
import scipy.ndimage
import os
import time

def load_data(path):
    """
    Load a JSON file and convert it into a pandas DataFrame.

    Parameters:
    path (str): The path to the JSON file.

    Returns:
    df (pd.DataFrame): The loaded data as a pandas DataFrame.
    """
    df = pd.read_json(path)
    return df


def get_SE_combinations():
    """
    Generate all possible combinations of structuring elements with repetition and length upto 4.

    Returns:
    list: The list of possible combinations of structuring elements.
    """
    SEs = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
    all_combinations = []

    for length in range(1, 5):
        for combination in itertools.product(SEs, repeat=length):
            all_combinations.append(combination)

    return all_combinations

# combinations = get_SE_combinations()
# print(combinations)

def get_SEs():
    """
    Define and return all structuring elements(SEs) in a dictionary format.

    Returns:
        dict: A dictionary of structuring elements, with keys as their name and values as corresponding 2D matrices.
    """
    SEs = {
        'SE1': [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
        'SE2': [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        'SE3': [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        'SE4': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        'SE5': [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
        'SE6': [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
        'SE7': [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
        'SE8': [[0, 0, 0], [0, 0, 0], [1, 1, 1]]
    }
    return SEs

# Get all structuring elements
# SEs = get_SEs()
#
# for key, SE in SEs.items():
#     print(f"{key} = {SE}")


def dilate_image(image, SE):
    """
    Apply binary dilation on an image with the given structuring element.

    Parameters:
    image (np.array): The original image.
    SE (np.array): The structuring element.

    Returns:
    (np.array): The dilated image.
    """
    # Convolution gives the effect of binary dilation
    dilated_image = scipy.signal.convolve2d(image, SE, mode='same', boundary='fill', fillvalue=0)

    # Set non-zero entries in dilated image to 1 to ensure binary image
    dilated_image[dilated_image > 0] = 1

    return dilated_image


def reduce_sequences(df, sequences, SEs):
    """
    Reduce the list of sequences by discarding those that do not produce the desired output.

    Parameters:
    df (pd.DataFrame): The dataframe with columns 'input' and 'output'.
    sequences (list): The list of sequences of structuring elements.
    SEs (dict): The dictionary of structuring elements.

    Returns:
    (list): The reduced list of sequences.
    """
    reduced_sequences = []
    # Iterate over each sequence
    for sequence in sequences:
        keep_sequence = True
        # Iterate over each row in the dataframe
        for _, row in df.iterrows():
            transformed_image = row['input']
            # Apply the dilation operation for each SE in the sequence
            for SE_name in sequence:
                transformed_image = dilate_image(transformed_image, SEs[SE_name])
            # Check if the transformed image matches the output (i.e. All active pixels in output should be active in the transformed image)
            keep_sequence = np.array_equal(np.logical_and(transformed_image, row['output']), row['output'])
            # Discard the sequence if it does not match
            if not keep_sequence:
                break
        if keep_sequence:
            reduced_sequences.append(sequence)

    return reduced_sequences

# r = reduce_sequences(data, combinations, SEs)
# print("Total sequences: ", len(combinations))
# print("Reduced sequences: ", len(r))
# print(r)


def erode_image(image, SE):
    """
    Apply binary erosion on an image with the given structuring element.

    Parameters:
    image (np.array): The original image.
    SE (np.array): The structuring element.

    Returns:
    (np.array): The eroded image.
    """
    # Binary erosion gives the effect of binary erosion
    eroded_image = scipy.ndimage.binary_erosion(image, structure=SE).astype(image.dtype)

    return eroded_image


def apply_operations(df, sequences, SEs):
    """
    Apply the dilation and erosion operation for each sequence and test if the transformed image matches the output.

    Parameters:
    df (pd.DataFrame): The dataframe with columns 'input' and 'output'.
    sequences (list): The list of sequences of structuring elements.
    SEs (dict): The dictionary of structuring elements.

    Returns:
    (list): The list of sequences for which the sequence of operations matches the output.
    """
    valid_sequences = []
    # Iterate over each sequence
    for sequence in sequences:
        is_sequence_valid = True
        # Iterate over each row in the dataframe
        for _, row in df.iterrows():
            # Stage 1: Dilation
            dilated_image = row['input']
            for SE_name in sequence:
                dilated_image = dilate_image(dilated_image, SEs[SE_name])
            # Stage 2: Erosion
            transformed_image = dilated_image
            for SE_name in sequence:
                transformed_image = erode_image(transformed_image, SEs[SE_name])
            # Check if the transformed image matches the output
            is_sequence_valid = np.array_equal(transformed_image, row['output'])
            # If the transformed image doesn't match the output for even one input, invalidate the sequence
            if not is_sequence_valid:
                break
        # Add the sequence to valid_sequences list if it's a valid sequence
        if is_sequence_valid:
            valid_sequences.append(sequence)

    return valid_sequences

# result = apply_operations(data, r, SEs)
# print(result)
# print("Total number of sequences that work: ", len(result))


def analyze_all_tasks(directory, sequences, SEs):
    """
    Apply operations to all the tasks in a directory and print the time taken for each task.
    Also save the sequence and time taken for each task in a csv file.

    Parameters:
    directory (str): The path to the directory containing the tasks.
    sequences (list): The list of sequences of structuring elements.
    SEs (dict): The dictionary of structuring elements.

    Returns:
    (list): The list of valid sequences for all tasks.
    """
    task_files = os.listdir(directory)
    json_files = [file for file in task_files if file.endswith(".json")]
    all_valid_sequences = []
    results = []

    for json_file in json_files:
        print(f"Analyzing task: {json_file}")
        task_path = os.path.join(directory, json_file)
        df = load_data(task_path)
        start_time = time.time()
        valid_sequences = apply_operations(df, sequences, SEs)
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken for {json_file}: {time_taken} seconds")

        all_valid_sequences.append((json_file, valid_sequences))
        results.append([json_file, valid_sequences, time_taken])

    # Create a DataFrame and save it as a csv file
    results_df = pd.DataFrame(results, columns=["Task", "Valid_Sequences", "Time_Taken"])
    results_df.to_csv("task_results_catA_simple.csv", index=False)

    return all_valid_sequences


directory = "../../../src/IPARC_ChallengeV2/Dataset/CatA_Simple/"
sequences = get_SE_combinations()
SEs = get_SEs()

start_time = time.time()
all_valid_sequences = analyze_all_tasks(directory, sequences, SEs)
end_time = time.time()

print(f"Total time taken: {end_time - start_time} seconds")
print("All valid sequences: ", all_valid_sequences)