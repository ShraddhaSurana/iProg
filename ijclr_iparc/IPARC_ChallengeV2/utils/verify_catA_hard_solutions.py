import numpy as np
import pandas as pd
from scipy.ndimage.morphology import binary_dilation, binary_erosion
import json
from IPARC_ChallengeV2.ListSelEm import list_se_3x3
from IPARC_ChallengeV2.Utils import Change_Colour, Process


def _perform_CatA_Hard(img, band, op, se):
    if band is not None:
        list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
        list_se_idx = list_se.index(se)
        if op == 'Dilation':
            return binary_dilation(img, list_se_3x3[list_se_idx])
        elif op == 'Erosion':
            return binary_erosion(img, list_se_3x3[list_se_idx])

    else:
        return Change_Colour(img, np.array(se, dtype=np.int32))


def verify_solution(tasks, list_ops):
    """
    Verify the solution for CatA_Simple tasks.
    :param tasks: List of tasks
    :param list_ops: List of operations
    :return: None
    """

    example_number = 1
    correctly_assessed = 1
    for d in tasks:
        img = np.array(d['input'], dtype=np.int32)
        img = Process(img, num_colors=3)
        for band, op, se in list_ops:
            if band is not None:
                img[:, :, band - 1] = _perform_CatA_Hard(img[:, :, band - 1], band, op, se)
            else:
                img = _perform_CatA_Hard(img, band, op, se)
        img = img * 1

        out = np.array(d['output'], dtype=np.int32)
        check_same = np.all(img == out)

        if check_same:
            print(f"Example: {example_number} Program works!!")
            correctly_assessed += 1
        else:
            print(f"Example number: {example_number} Something went wrong!!")
        example_number += 1
    if example_number == correctly_assessed:
        print("All examples passed.")


if __name__ == '__main__':
    read_all_solutions_from_file = True
    if read_all_solutions_from_file:
        # Load CSV
        # csv_file = "../solutions/task_results_catA_hard.csv"  # Replace with your actual CSV file path
        csv_file = "../solutions/task_results_catA_Hard_with_snapshots_catC.csv"  # Replace with your actual CSV file path
        df = pd.read_csv(csv_file)

        # Iterate through each task
        for _, row in df.iterrows():
            task_filename = row["task_id"]
            task_index = int(task_filename.split(".")[0][4:])  # Extract task number
            print(f"Task: {task_index}")

            list_ops = json.loads(row["solution"])

            # Load the dataset
            catA_path = f"../Dataset/CatA_Hard/Task{task_index:03d}.json"
            with open(catA_path, 'r') as f:
                tasks = json.load(f)
            verify_solution(tasks, list_ops)
    else:
        task_index = 92  # Example Number
        # Will have to replace null with None in the solution here as null isn ot a default in python
        list_ops = [[1, "Dilation", "SE1"], [1, "Dilation", "SE2"], [1, "Dilation", "SE4"], [1, "Dilation", "SE6"], [1, "Erosion", "SE1"], [1, "Erosion", "SE2"], [1, "Erosion", "SE4"], [1, "Erosion", "SE6"], [2, "Dilation", "SE1"], [2, "Dilation", "SE1"], [2, "Dilation", "SE2"], [2, "Dilation", "SE4"], [2, "Erosion", "SE1"], [2, "Erosion", "SE1"], [2, "Erosion", "SE2"], [2, "Erosion", "SE4"], [3, "Dilation", "SE2"], [3, "Dilation", "SE7"], [3, "Dilation", "SE4"], [3, "Dilation", "SE7"], [3, "Erosion", "SE2"], [3, "Erosion", "SE7"], [3, "Erosion", "SE4"], [3, "Erosion", "SE7"], [None, "color_rule", [[0, 0, 0, 0], [0, 0, 1, 1], [0, 1, 0, 2], [0, 1, 1, 1], [1, 0, 0, 1], [1, 0, 1, 3], [1, 1, 0, 1], [1, 1, 1, 1]]]]

        print(f"Task: {task_index}")

        # Load the dataset
        catA_path = "../Dataset/CatA_Hard/Task{:03d}"
        with open((catA_path + ".json").format(task_index), 'r') as f:
            tasks = json.load(f)
        # Load the solution.
        # with open((catA_path + "_soln.json").format(task_index), 'r') as f:
        #     list_ops = json.load(f)

        verify_solution(tasks, list_ops)