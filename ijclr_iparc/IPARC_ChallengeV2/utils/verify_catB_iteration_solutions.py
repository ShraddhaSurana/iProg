import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.ndimage.morphology import binary_dilation, binary_erosion
import json
from IPARC_ChallengeV2.ListSelEm import list_se_3x3


def _perform_CatB_Iteration(img, n_iterate, op, se):
    for _ in range(n_iterate):
        list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
        list_se_idx = list_se.index(se)
        if op == 'Dilation':
            img = binary_dilation(img, list_se_3x3[list_se_idx])
        elif op == 'Erosion':
            img = binary_erosion(img, list_se_3x3[list_se_idx])
    return img


def verify_solution(tasks, list_ops):
    """
    Verify the solution for CatB_Sequence tasks.
    :param tasks: List of tasks
    :param list_ops: List of operations
    :return: None
    """
    example_number = 1
    correctly_assessed = 1

    for d in tasks:
        img = np.array(d['input'], dtype=np.int32)
        for subtask, n_iterate, op, se in list_ops:
            if d['subtask'] == subtask:
                img = _perform_CatB_Iteration(img, n_iterate, op, se)
                # plt.imshow(img, cmap='gray')
                # plt.title("Transformed")
                # plt.show()
        img = img*1

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
        return True

if __name__ == '__main__':
    read_all_solutions_from_file = True
    if read_all_solutions_from_file:
        count = 0
        # Load CSV
        csv_file = "../solutions/task_results_catB_iteration.csv"
        df = pd.read_csv(csv_file)
        failed_tasks = []
        # Iterate through each task
        for _, row in df.iterrows():
            task_filename = row["task_id"]
            # task_index = row["Task"]  # Extract task number
            valid_sequences = eval(row["solution_json"])  # Convert string to list of tuples

            # Load the dataset
            catB_iteration = f"../Dataset/CatB_Iteration/{task_filename}.json"
            with open(catB_iteration, 'r') as f:
                tasks = json.load(f)

            print(f"{task_filename}")
            success = verify_solution(tasks, valid_sequences)
            if success:
                count +=1
            else:
                failed_tasks.append(task_filename)
        print(f"Success: {count}")
        print(failed_tasks)

    else:
        task_index = 0
        list_ops = [[0, 1, "Dilation", "SE4"], [0, 1, "Dilation", "SE5"], [0, 1, "Erosion", "SE4"], [0, 1, "Erosion", "SE5"], [0, 4, "Dilation", "SE6"], [0, 4, "Erosion", "SE6"], [1, 1, "Dilation", "SE1"], [1, 1, "Dilation", "SE6"], [1, 1, "Erosion", "SE1"], [1, 1, "Erosion", "SE6"], [1, 4, "Dilation", "SE6"], [1, 4, "Erosion", "SE6"], [2, 1, "Dilation", "SE2"], [2, 1, "Dilation", "SE5"], [2, 1, "Erosion", "SE2"], [2, 1, "Erosion", "SE5"], [2, 4, "Dilation", "SE6"], [2, 4, "Erosion", "SE6"]]

        print(f"Task: {task_index}")
        with open("../Dataset/CatB_Iteration/Task{:03d}.json".format(task_index), 'r') as f:
            tasks = json.load(f)

        verify_solution(tasks, list_ops)
