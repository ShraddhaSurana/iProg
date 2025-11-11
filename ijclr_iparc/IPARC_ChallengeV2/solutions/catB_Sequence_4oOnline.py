"""
Code created using onlint chat interface with GPT 4o - asking to create DFD and follow it to create the code.
"""
from collections import defaultdict
from typing import List, Tuple, Dict

import numpy as np

def load_task_data(task_json_path: str) -> Dict[int, List[Tuple[np.ndarray, np.ndarray]]]:
    """
    Loads an IPARC task file and groups (input, output) image pairs by subtask.

    Parameters:
    - task_json_path (str): Path to the JSON file containing the task.

    Returns:
    - Dict[int, List[Tuple[np.ndarray, np.ndarray]]]: A dictionary mapping each subtask id
      to a list of (input, output) image pairs as NumPy arrays.
    """
    with open(task_json_path, 'r') as f:
        data = json.load(f)

    subtasks = defaultdict(list)
    for example in data:
        input_image = np.array(example["input"], dtype=np.uint8)
        output_image = np.array(example["output"], dtype=np.uint8)
        subtask_id = example["subtask"]
        subtasks[subtask_id].append((input_image, output_image))

    return dict(subtasks)


def extract_binary_masks(
    subtasks: Dict[int, List[Tuple[np.ndarray, np.ndarray]]]
) -> Dict[int, List[Tuple[np.ndarray, np.ndarray]]]:
    """
    Converts all images in each subtask to binary masks.

    Parameters:
    - subtasks (Dict[int, List[Tuple[np.ndarray, np.ndarray]]]):
      Dictionary of subtask id to list of (input, output) image pairs.

    Returns:
    - Dict[int, List[Tuple[np.ndarray, np.ndarray]]]:
      Dictionary of subtask id to binary (input, output) mask pairs.
    """
    binarized = {}
    for subtask_id, io_pairs in subtasks.items():
        binarized[subtask_id] = []
        for input_img, output_img in io_pairs:
            bin_input = (input_img != 0).astype(np.uint8)
            bin_output = (output_img != 0).astype(np.uint8)
            binarized[subtask_id].append((bin_input, bin_output))
    return binarized

def get_structuring_elements() -> Dict[str, np.ndarray]:
    """
    Returns a dictionary of 3x3 structuring elements as defined by the user.
    """
    return {
        'SE1': np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], dtype=bool),
        'SE2': np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
        'SE3': np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool),
        'SE4': np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=bool),
        'SE5': np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]], dtype=bool),
        'SE6': np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]], dtype=bool),
        'SE7': np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=bool),
        'SE8': np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]], dtype=bool)
    }


def generate_flexible_sequences(
        max_steps: int = 8
) -> List[List[Tuple[str, str]]]:
    """
    Generates all sequences of length `max_steps` with arbitrary
    combinations of Dilation/Erosion and user-defined structuring elements.

    Parameters:
    - max_steps (int): Number of operations in the sequence.

    Returns:
    - List[List[Tuple[str, str]]]: Sequences of operations.
    """
    from itertools import product

    ops = ["Dilation", "Erosion"]
    se_names = list(get_structuring_elements().keys())

    # All (op, SE) pairs
    op_se_pairs = list(product(ops, se_names))

    # Generate all sequences of length `max_steps`
    sequences = list(product(op_se_pairs, repeat=max_steps))

    # Convert tuples-of-tuples to list-of-tuples
    return [list(seq) for seq in sequences]

from typing import List, Tuple
import itertools

def generate_valid_sequences_with_patterns() -> List[List[Tuple[str, str]]]:
    """
    Generates valid 8-step operation sequences with structure:
    - Prefix: D, D, E, E
    - Postfix: D, D, E, E
    - Erosions reuse the SE of the Dilation directly before

    Returns:
    - List of 8-step sequences, each a list of (operation, SE_name) tuples
    """
    se_names = list(get_structuring_elements().keys())

    # Choose SEs for 2 prefix Dilations and 2 postfix Dilations
    sequences = []
    for prefix_d1, prefix_d2, postfix_d1, postfix_d2 in itertools.product(se_names, repeat=4):
        sequence = [
            ("Dilation", prefix_d1),
            ("Dilation", prefix_d2),
            ("Erosion", prefix_d1),  # mirror of prefix_d1
            ("Erosion", prefix_d2),  # mirror of prefix_d2
            ("Dilation", postfix_d1),
            ("Dilation", postfix_d2),
            ("Erosion", postfix_d1),  # mirror of postfix_d1
            ("Erosion", postfix_d2)   # mirror of postfix_d2
        ]
        sequences.append(sequence)

    return sequences

from scipy.ndimage import binary_dilation, binary_erosion

def apply_operation(image: np.ndarray, operation: str, se: np.ndarray) -> np.ndarray:
    """
    Applies a single morphological operation to a binary image.

    Parameters:
    - image (np.ndarray): Binary image (0s and 1s)
    - operation (str): "Dilation" or "Erosion"
    - se (np.ndarray): Structuring element (3x3, dtype=bool)

    Returns:
    - np.ndarray: Transformed binary image
    """
    if operation == "Dilation":
        return binary_dilation(image, structure=se).astype(np.uint8)
    elif operation == "Erosion":
        return binary_erosion(image, structure=se).astype(np.uint8)
    else:
        raise ValueError(f"Unsupported operation: {operation}")


def apply_sequence(image: np.ndarray, sequence: List[Tuple[str, str]]) -> np.ndarray:
    """
    Applies a full 8-step sequence of operations to a binary image.

    Parameters:
    - image (np.ndarray): Binary input image
    - sequence (List[Tuple[str, str]]): List of (operation, SE_name)

    Returns:
    - np.ndarray: Final binary image after applying all operations
    """
    se_bank = get_structuring_elements()
    result = image.copy()

    for op, se_name in sequence:
        se = se_bank[se_name]
        result = apply_operation(result, op, se)

    return result


def sequence_matches_all_examples(
    sequence: List[Tuple[str, str]],
    io_pairs: List[Tuple[np.ndarray, np.ndarray]]
) -> bool:
    """
    Checks whether a given sequence matches all input-output pairs exactly.

    Parameters:
    - sequence: The operation sequence to test
    - io_pairs: List of (input, output) binary image pairs

    Returns:
    - bool: True if the sequence transforms all inputs to matching outputs
    """
    for input_img, expected_output in io_pairs:
        predicted_output = apply_sequence(input_img, sequence)
        if not np.array_equal(predicted_output, expected_output):
            return False
    return True

def find_solution_across_subtasks(
    subtasks: Dict[int, List[Tuple[np.ndarray, np.ndarray]]]
) -> List[List[Tuple[str, str]]]:
    """
    Finds a valid 8-step solution for each subtask using a shared postfix.

    Parameters:
    - subtasks: Dictionary of subtask_id to input-output image pairs

    Returns:
    - List of full 8-step sequences for each subtask (same postfix, varying prefix)
      OR empty list if no common postfix works
    """
    se_names = list(get_structuring_elements().keys())

    # Generate all valid postfixes (2D + 2E with SE mirror)
    postfixes = [
        [("Dilation", d1), ("Dilation", d2),
         ("Erosion", d1), ("Erosion", d2)]
        for d1, d2 in itertools.product(se_names, repeat=2)
    ]

    for postfix in postfixes:
        subtask_solutions = []
        for subtask_id, io_pairs in subtasks.items():
            found = False
            # Try all 2D + 2E prefixes
            for d1, d2 in itertools.product(se_names, repeat=2):
                prefix = [("Dilation", d1), ("Dilation", d2),
                          ("Erosion", d1), ("Erosion", d2)]
                full_seq = prefix + postfix
                if sequence_matches_all_examples(full_seq, io_pairs):
                    subtask_solutions.append(full_seq)
                    found = True
                    break  # Stop after first matching prefix
            if not found:
                break  # This postfix fails, move to next
        if len(subtask_solutions) == len(subtasks):
            return subtask_solutions  # Found working solution for all subtasks

    return []  # No working postfix found

import os
import time
import pandas as pd
import json

def solve_task_file(filepath: str) -> Tuple[str, List[List]]:
    """
    Solves a single task file and returns the formatted solution and time taken.

    Parameters:
    - filepath: Path to a task JSON file.

    Returns:
    - Tuple of (task_name, solution_steps_list, time_taken)
    """
    task_name = os.path.splitext(os.path.basename(filepath))[0]
    subtasks = load_task_data(filepath)
    subtasks_bin = extract_binary_masks(subtasks)

    start_time = time.time()
    solutions = find_solution_across_subtasks(subtasks_bin)
    elapsed = time.time() - start_time

    if not solutions:
        return task_name, [], elapsed

    # Format: [subtask_id, operation, SE_name]
    formatted = []
    for subtask_id, steps in enumerate(solutions):
        formatted += [[subtask_id, op, se] for op, se in steps]

    return task_name, formatted, elapsed


def solve_all_tasks_in_folder(folder_path: str, output_csv: str):
    """
    Solves all JSON tasks in the given folder and saves results to a CSV file.

    Parameters:
    - folder_path: Path containing task JSON files.
    - output_csv: Output CSV filename.
    """
    results = []

    for filename in os.listdir(folder_path):
        if filename.startswith("Task") and filename.endswith(".json") and "_soln" not in filename:
            filepath = os.path.join(folder_path, filename)
            print(f"Solving: {filename}")
            task_name, solution, duration = solve_task_file(filepath)
            results.append({
                "task_id: task_name,
                "solution": json.dumps(solution),
                "time_taken": round(duration, 3)
            })

    # Save as CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ All results saved to {output_csv}")


if __name__ == "__main__":
    solve_all_tasks_in_folder("../../../src/IPARC_ChallengeV2/Dataset/CatB_Sequence",
                              "catB_sequence_solutions.csv")