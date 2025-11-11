"""
Created using iStrucInd with API calls to ChatGPT-4.0 & a little of 4o as well.
"""
import pandas as pd
import json
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion
import os
import time
import re

def load_data(path: str) -> pd.DataFrame:
    """Load dataset from the specified JSON file."""
    with open(path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    return df


def split_subproblems(df: pd.DataFrame) -> dict:
    """Split data into subproblems based on the subtask column."""
    subproblems = {}
    for subtask in df['subtask'].unique():
        subproblems[f'subtask{subtask}'] = df[df['subtask'] == subtask]
    return subproblems


def get_structuring_elements() -> dict:
    """Return the predefined structuring elements as a dictionary."""
    SE1 = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    SE2 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    SE3 = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    SE4 = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    SE5 = np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
    SE6 = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]])
    SE7 = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]])
    SE8 = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])

    se_dict = {
        "SE1": SE1,
        "SE2": SE2,
        "SE3": SE3,
        "SE4": SE4,
        "SE5": SE5,
        "SE6": SE6,
        "SE7": SE7,
        "SE8": SE8,
    }

    return se_dict


def morphological_process(image, operation, se):
    """Process the image using the specified morphological operation and structuring element."""
    if operation == "Dilation":
        return binary_dilation(image, structure=se).astype(image.dtype)
    elif operation == "Erosion":
        return binary_erosion(image, structure=se).astype(image.dtype)
    else:
        raise ValueError("Unsupported operation")


def generate_transformation_sequence(input_img, output_img, structuring_elements):
    """Generate valid sequences of transformations that map the input image to the output image."""
    sequences = []
    operations = ["Dilation", "Erosion"]

    for se_key1, se1 in structuring_elements.items():
        for se_key2, se2 in structuring_elements.items():
            img_1 = morphological_process(input_img, "Dilation", se1)
            img_2 = morphological_process(img_1, "Dilation", se2)
            img_3 = morphological_process(img_2, "Erosion", se1)
            img_4 = morphological_process(img_3, "Erosion", se2)

            for se_key3, se3 in structuring_elements.items():
                for se_key4, se4 in structuring_elements.items():
                    img_5 = morphological_process(img_4, "Dilation", se3)
                    img_6 = morphological_process(img_5, "Dilation", se4)
                    img_7 = morphological_process(img_6, "Erosion", se3)
                    img_8 = morphological_process(img_7, "Erosion", se4)

                    if np.array_equal(img_8, output_img):
                        sequence = [
                            ["Dilation", se_key1], ["Dilation", se_key2],
                            ["Erosion", se_key1], ["Erosion", se_key2],
                            ["Dilation", se_key3], ["Dilation", se_key4],
                            ["Erosion", se_key3], ["Erosion", se_key4]
                        ]
                        sequences.append(sequence)

    return sequences


def validate_sequence(sequence, input_img, output_img, structuring_elements):
    """Validate if the given sequence transforms the input image to the output image."""
    img = input_img
    for operation, se_key in sequence:
        img = morphological_process(img, operation, structuring_elements[se_key])

    return np.array_equal(img, output_img)


def generate_solution_subtask0(subproblems, structuring_elements):
    """Generate all valid sequences for each subproblem."""
    solutions = []
    for subtask_id, subproblem_df in subproblems.items():
        valid_sequences = []
        subtask_id_int = int(subtask_id.replace('subtask', ''))
        # Get sequences using the first input-output pair
        input_img = np.array(subproblem_df.iloc[0]['input'])
        output_img = np.array(subproblem_df.iloc[0]['output'])
        sequences = generate_transformation_sequence(input_img, output_img, structuring_elements)
        # Validate these sequences with all images in the subtask
        for sequence in sequences:
            is_valid = True
            for idx, row in subproblem_df.iterrows():
                input_img = np.array(row['input'])
                output_img = np.array(row['output'])
                if not validate_sequence(sequence, input_img, output_img, structuring_elements):
                    is_valid = False
                    break
            if is_valid:
                valid_sequences.append(sequence)
        solutions.extend(valid_sequences)
    return solutions

from itertools import combinations, product


def find_solutions(subproblem_df, solutions_subtask1, structuring_elements):
    # Generating all unique combinations of 2 structuring elements as we have to select 2 out of 8 SEs
    unique_combinations = list(product(structuring_elements.keys(), repeat=2))
    solutions_subtask2 = []

    fixed_parts = [tuple(tuple(step) for step in solution[4:]) for solution in solutions_subtask1]
    unique_fixed_sequences = list(set(fixed_parts))
    unique_fixed_sequences = [[list(step) for step in sequence] for sequence in unique_fixed_sequences]
    # Step 4: Iterate
    for fixed_sequence in unique_fixed_sequences:
        # If you want to use it as a list again:
        fixed_sequence = list(fixed_sequence)

        for combination in unique_combinations:
            # Create a new sequence starting with 2 Dilation operations followed by 2 Erosion operations
            # For both Dilation and Erosion operations the structs used are same but in reverse order.
            new_sequence = [['Dilation', combination[0]], ['Dilation', combination[1]], ['Erosion', combination[0]],
                            ['Erosion', combination[1]]] + fixed_sequence
            # Validate the new sequence and only add to solutions_subtask2 when it works
            is_valid = True
            for idx, row in subproblem_df.iterrows():
                input_img = np.array(row['input'])
                output_img = np.array(row['output'])

                if not validate_sequence(new_sequence, input_img, output_img, structuring_elements):
                    is_valid = False
                    break

            if is_valid:
                solutions_subtask2.append(new_sequence)

    return solutions_subtask2


def find_common_sequences(solutions1, solutions2, solutions3):
    """
    Function that identifies and returns the sequences from each of the given subtask solutions that end with the same sequences.

    Parameters:

    solutions1 : list (A list of sequences for subtask 1)
    solutions2 : list (A list of sequences for subtask 2)
    solutions3 : list (A list of sequences for subtask 3)

    Returns:

    list: A list of sequences from each subtask for which the last four sequences are the same, each sequence prepended by its subtask id
    """

    # Iterate all solutions for subtask1
    for solution1 in solutions1:

        # Get the last 4 sequences of solution1
        last4_solution1 = solution1[-4:]

        # Check these last 4 sequences with all solutions of subtask2 and subtask3
        for solution2 in solutions2:
            for solution3 in solutions3:
                # If another solution from subtask2 & 3 ends with the same last 4 sequences, then return these sequences along with their subtask id
                if last4_solution1 == solution2[-4:] == solution3[-4:]:
                    return [[0] + seq for seq in solution1] + [[1] + seq for seq in solution2] + [[2] + seq for seq in
                                                                                                  solution3]

    return []  # If no output has been returned up to here, return an empty list

def process_task(file_path, structuring_elements):
    # Load data
    with open(file_path) as f:
        task_dict = json.load(f)
    df = pd.DataFrame(task_dict)
    # Split into subproblems
    subproblems = split_subproblems(df)
    # Generate solutions for each subtask
    solutions_subtask0 = generate_solution_subtask0({'subtask0': subproblems['subtask0']}, structuring_elements)
    # print("--1--")
    # print(len(solutions_subtask0))
    # print(solutions_subtask0)
    # print("==end 1--==")
    solutions_subtask1 = find_solutions(subproblems['subtask1'], solutions_subtask0, structuring_elements)
    # print("--2--")
    # print(len(solutions_subtask1))
    # print(solutions_subtask1)
    solutions_subtask2 = find_solutions(subproblems['subtask2'], solutions_subtask1, structuring_elements)
    # print("--3--")
    # print(len(solutions_subtask2))
    # print(solutions_subtask2)
    result = find_common_sequences(solutions_subtask0, solutions_subtask1, solutions_subtask2)
    print("----")
    print(result)
    return result

if __name__ == "__main__":
    # Path to the dataset
    dir_path = "../../../src/IPARC_ChallengeV2/Dataset/CatB_Sequence/"
    # Get structuring elements
    structuring_elements = get_structuring_elements()
    # Prepare a pandas DataFrame for all results
    results_df = pd.DataFrame(columns=['task_id', 'solution', 'time_taken'])
    # Loop over all task files in the directory
    row_count = 0
    for filename in os.listdir(dir_path):
        if re.match('Task[0-9]{3}.json$', filename):
            task_id = filename[4:-5]  # Strip 'Task' and '.json'
            print(task_id)
            # Measure the start time
            start_time = time.time()
            # Process the task file
            solution = process_task(os.path.join(dir_path, filename), structuring_elements)
            # Measure time taken
            time_taken = time.time() - start_time
            # Append results to DataFrame
            results_df.loc[row_count] = [task_id, str(solution).replace("'", "\""), time_taken]
            row_count += 1
    # Save results to a CSV file
    results_df.to_csv('task_solutions_catB_sequence.csv', index=False)