"""
Use ChatGPT 4o to solve the IPARC Challenge V2 Category B Iteration. It came up with the structuring and then create code for each module.
"""
import os
import time
import json
import pandas as pd
import numpy as np

from typing import Any, List, Tuple, Optional, Dict
from itertools import product
from collections import defaultdict
from pathlib import Path
from scipy.ndimage import binary_dilation, binary_erosion

# Type alias
Image = List[List[int]]

# Structuring Elements (fixed to match user's specification)
SEs = {
    'SE1': np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], dtype=bool),
    'SE2': np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
    'SE3': np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool),
    'SE4': np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=bool),
    'SE5': np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]], dtype=bool),
    'SE6': np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]], dtype=bool),
    'SE7': np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=bool),
    'SE8': np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]], dtype=bool)
}

def apply_operation(img: np.ndarray, op: str, se_name: str) -> np.ndarray:
    se = SEs[se_name]
    if op == "Dilation":
        return binary_dilation(img, structure=se).astype(int)
    elif op == "Erosion":
        return binary_erosion(img, structure=se).astype(int)
    else:
        raise ValueError(f"Invalid operation: {op}")

def image_to_binary(img: Image) -> np.ndarray:
    return np.array(img, dtype=bool)

def find_shared_loop_and_per_subtask_pres(
    task_subtasks: Dict[int, List[Tuple[Image, Image]]],
    max_k: int = 4,
    debug: bool = False
) -> Optional[Tuple[Dict[int, List[Tuple[str, str]]], int, Tuple[str, str]]]:
    all_subtask_ids = list(task_subtasks.keys())

    for se_loop in SEs:
        for k in range(1, max_k + 1):
            all_pres: Dict[int, List[Tuple[str, str]]] = {}
            valid_loop = True

            for sub_id in all_subtask_ids:
                pairs = task_subtasks[sub_id]
                found_pre = False

                for se1, se2 in product(SEs.keys(), repeat=2):
                    pre_seq = [
                        ("Dilation", se1), ("Dilation", se2),
                        ("Erosion", se1), ("Erosion", se2)
                    ]

                    success = True
                    for input_img, output_img in pairs:
                        input_bin = image_to_binary(input_img)
                        target_bin = np.array(output_img)

                        img = input_bin.copy()
                        for op, se in pre_seq:
                            img = apply_operation(img, op, se)
                        for _ in range(k):
                            img = apply_operation(img, "Dilation", se_loop)
                        for _ in range(k):
                            img = apply_operation(img, "Erosion", se_loop)

                        if not np.array_equal(img.astype(int), target_bin.astype(int)):
                            success = False
                            break

                    if success:
                        all_pres[sub_id] = pre_seq
                        found_pre = True
                        break

                if not found_pre:
                    valid_loop = False
                    break

            if valid_loop:
                return all_pres, k, ("Dilation", se_loop)

    return None

# Function to solve one task
def solve_one_task(task_file: Path) -> Tuple[str, float, Optional[List[List[Any]]]]:
    task_id = task_file.stem
    with open(task_file, 'r') as f:
        task_data = json.load(f)

    subtasks = defaultdict(list)
    for example in task_data:
        sub_id = example.get("subtask", 0)
        subtasks[sub_id].append((example["input"], example["output"]))

    start = time.time()
    result = find_shared_loop_and_per_subtask_pres(subtasks, debug=False)
    end = time.time()
    time_taken = round(end - start, 4)

    if result is None:
        return task_id, time_taken, None

    all_pres, k, (loop_op, loop_se) = result
    solution = []
    for sub_id, pre_seq in all_pres.items():
        for op, se in pre_seq:
            solution.append([sub_id, 1, op, se])
        solution.append([sub_id, k, "Dilation", loop_se])
        solution.append([sub_id, k, "Erosion", loop_se])

    return task_id, time_taken, solution

if __name__ == "__main__":
    # Run for Task000 to Task099
    base_dir = Path("../../../src/IPARC_ChallengeV2/Dataset/CatB_Iteration")
    results = []
    for i in range(100):
        task_filename = f"Task{i:03}.json"
        task_path = base_dir / task_filename
        if not task_path.exists():
            continue

        task_id, time_taken, solution = solve_one_task(task_path)
        solution_json = json.dumps(solution) if solution else "None"
        results.append({
            "task_id": task_id,
            "solution": solution_json,
            "time_taken": time_taken
        })

    # Save to CSV
    df = pd.DataFrame(results)
    csv_path = "task_results_catB_iteration.csv"
    df.to_csv(csv_path, index=False)
