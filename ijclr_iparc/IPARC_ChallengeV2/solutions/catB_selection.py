# Re-import everything due to kernel reset
import numpy as np
import json
import time
import itertools
import os
import csv
from typing import List, Tuple, Union, Dict
from scipy.ndimage import binary_dilation, binary_erosion, binary_hit_or_miss


STRUCTURING_ELEMENTS = {
    'SE1': np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], dtype=bool),
    'SE2': np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
    'SE3': np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool),
    'SE4': np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=bool),
    'SE5': np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]], dtype=bool),
    'SE6': np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]], dtype=bool),
    'SE7': np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=bool),
    'SE8': np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]], dtype=bool),
}


def load_task_data(path: str) -> List[Dict[str, np.ndarray]]:
    with open(path, "r") as f:
        task = json.load(f)
    return [{"input": np.array(ex["input"]), "output": np.array(ex["output"])} for ex in task]


def extract_foreground(image: np.ndarray) -> np.ndarray:
    return (image > 0).astype(np.uint8)


def apply_hit_or_miss_colored(image: np.ndarray, se: np.ndarray) -> np.ndarray:
    fg = extract_foreground(image)
    mask = binary_hit_or_miss(fg, structure1=(se == 1), structure2=(se == 0)).astype(np.uint8)
    new_image = fg.copy()
    new_image[mask == 1] = 2
    return new_image


def split_bands_by_hit_or_miss_colored(image_with_selection: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    band1 = (image_with_selection == 1).astype(np.uint8)
    band2 = (image_with_selection == 2).astype(np.uint8)
    return band1, band2


def apply_structural_ops(band: np.ndarray, op_seq: List[Tuple[str, str]]) -> np.ndarray:
    result = band.copy()
    for op, se_name in op_seq:
        se = STRUCTURING_ELEMENTS[se_name]
        if op == "Dilation":
            result = binary_dilation(result, structure=se).astype(np.uint8)
        elif op == "Erosion":
            result = binary_erosion(result, structure=se).astype(np.uint8)
        else:
            raise ValueError(f"Unsupported operation: {op}")
    return result


def generate_band1_sequences(se_keys: List[str]) -> List[List[Tuple[str, str]]]:
    return [
        [("Dilation", se1), ("Dilation", se2), ("Erosion", se1), ("Erosion", se2)]
        for se1, se2 in itertools.product(se_keys, repeat=2)
    ]


def generate_band2_sequences(se_keys: List[str]) -> List[List[Tuple[str, str]]]:
    return [
        [("Dilation", se1), ("Dilation", se2), ("Dilation", se3), ("Erosion", se2), ("Erosion", se3)]
        for se1, se2, se3 in itertools.product(se_keys, repeat=3)
    ]


def learn_unified_color_rule(band1_list: List[np.ndarray], band2_list: List[np.ndarray], output_list: List[np.ndarray]) -> List[List[int]]:
    rule_dict = {(0, 0): 0}
    for b1, b2, out in zip(band1_list, band2_list, output_list):
        pairs = set(zip(b1.flatten(), b2.flatten())) - {(0, 0)}
        for i, j in pairs:
            if (i, j) not in rule_dict:
                mask = (b1 == i) & (b2 == j)
                values = out[mask]
                if len(values):
                    rule_dict[(i, j)] = int(np.bincount(values).argmax())
    return [[i, j, c] for (i, j), c in rule_dict.items()]


def apply_color_mapping(band1: np.ndarray, band2: np.ndarray, rule: List[List[int]]) -> np.ndarray:
    h, w = band1.shape
    merged = np.zeros((h, w), dtype=np.uint8)
    rule_dict = {(i, j): c for i, j, c in rule}
    for i in range(h):
        for j in range(w):
            merged[i, j] = rule_dict.get((band1[i, j], band2[i, j]), 0)
    return merged

# Resume the unified color rule search logic
def search_pipeline_with_unified_color_rule(task: List[Dict[str, np.ndarray]]) -> Tuple:
    se_keys = list(STRUCTURING_ELEMENTS.keys())
    band1_seqs = generate_band1_sequences(se_keys)
    band2_seqs = generate_band2_sequences(se_keys)

    print(f"Cross-example color rule search: {len(se_keys)} SEs × {len(band1_seqs)} B1 × {len(band2_seqs)} B2")

    for se_name in se_keys:
        se = STRUCTURING_ELEMENTS[se_name]

        for b1_ops in band1_seqs:
            for b2_ops in band2_seqs:
                band1_all, band2_all, output_all = [], [], []
                match = True

                for ex in task:
                    inp, out = np.array(ex["input"]), np.array(ex["output"])
                    marked = apply_hit_or_miss_colored(inp, se)
                    band1, band2 = split_bands_by_hit_or_miss_colored(marked)

                    band1 = apply_structural_ops(band1, b1_ops)
                    if np.any((band1 == 1) & (extract_foreground(out) == 0)):
                        match = False
                        break

                    band2 = apply_structural_ops(band2, b2_ops)
                    if np.any((band2 == 1) & (extract_foreground(out) == 0)):
                        match = False
                        break

                    band1_all.append(band1)
                    band2_all.append(band2)
                    output_all.append(out)

                if match:
                    # Learn a unified rule from all examples
                    unified_rule = learn_unified_color_rule(band1_all, band2_all, output_all)

                    # Verify the unified rule works for all examples
                    for b1, b2, out in zip(band1_all, band2_all, output_all):
                        pred = apply_color_mapping(b1, b2, unified_rule)
                        if not np.array_equal(pred, out):
                            match = False
                            break

                    if match:
                        print("✅ Verified: unified color rule works for all examples.")
                        return se_name, b1_ops, b2_ops, unified_rule

    print("❌ No universal solution found with consistent color rule.")
    return "None", [], [], []


def format_solution_json(hitmiss_se, band1_ops, band2_ops, color_rule):
    solution = [[None, "Hit-Or-Miss", str(hitmiss_se)]]
    solution += [[1, str(op), str(se)] for op, se in band1_ops]
    solution += [[2, str(op), str(se)] for op, se in band2_ops]
    solution += [[None, "change_color", [[int(i), int(j), int(c)] for i, j, c in color_rule]]]
    return solution


def run_all_tasks(task_dir, output_csv):
    with open(output_csv, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["task_id", "solution", "time_taken"])

        for file in sorted(os.listdir(task_dir)):
            if file.startswith("Task") and file.endswith(".json") and "_soln" not in file:
                task_path = os.path.join(task_dir, file)
                print(f"🔍 Processing {file}...")

                start = time.time()
                task_data = load_task_data(task_path)
                hitmiss_se, b1_ops, b2_ops, color_rule = search_pipeline_with_unified_color_rule(task_data)
                end = time.time()

                if hitmiss_se != "None":
                    solution_json = format_solution_json(hitmiss_se, b1_ops, b2_ops, color_rule)
                    writer.writerow([file, json.dumps(solution_json), round(end - start, 2)])
                else:
                    writer.writerow([file, "null", round(end - start, 2)])

                print(f"✅ Done {file} in {end - start:.2f}s")

if __name__ == "__main__":
    task_directory = "../../../src/IPARC_ChallengeV2/Dataset/CatB_Selection/"
    output_csv = "catB_selection_solutions.csv"
    run_all_tasks(task_directory, output_csv)
    print(f"\n📄 All results saved to: {output_csv}")


