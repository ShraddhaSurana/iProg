import numpy as np
import pandas as pd
from scipy.ndimage.morphology import binary_dilation, binary_erosion, binary_hit_or_miss
import json
from IPARC_ChallengeV2.ListSelEm import list_se_3x3


def _perform_CatA_Simple(img, op, se):
    list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
    list_se_idx = list_se.index(se)
    if op == 'Dilation':
        return binary_dilation(img, list_se_3x3[list_se_idx])
    elif op == 'Erosion':
        return binary_erosion(img, list_se_3x3[list_se_idx])


def verify_solution(tasks, list_ops):
    """
    Verify the solution for CatA_Simple tasks.
    :param tasks: List of tasks
    :param list_ops: List of operations
    :return: None
    """
    list_ops = [x.split() for x in list_ops]
    example_number = 1
    correctly_assessed = 1
    for example in tasks:
        img = np.array(example['input'], dtype=np.int32)
        for op, se in list_ops:
            img = _perform_CatA_Simple(img, op, se)
        img = img * 1

        out = np.array(example['output'], dtype=np.int32)
        check_same = np.all(img == out)
        if check_same:
            print(f"Example: {example_number} Program works!!")
            correctly_assessed+=1
        else:
            print(f"Example number: {example_number} Something went wrong!!")
        example_number+=1
    if example_number == correctly_assessed:
        print("All examples passed.")


if __name__ == '__main__':
    read_all_solutions_from_file = False
    if read_all_solutions_from_file:
        # Load CSV
        csv_file = "../solutions/task_results_catA_simple.csv"  # Replace with your actual CSV file path
        df = pd.read_csv(csv_file)

        # Iterate through each task
        for _, row in df.iterrows():
            task_filename = row["Task"]
            task_index = int(task_filename.split(".")[0][4:])  # Extract task number
            valid_sequences = eval(row["Valid_Sequences"])  # Convert string to list of tuples

            # Load the dataset
            catA_path = f"../Dataset/CatA_Simple/Task{task_index:03d}.json"
            with open(catA_path, 'r') as f:
                tasks = json.load(f)

            print(f"Task: {task_index}")

            # Test each sequence
            for seq in valid_sequences:
                list_ops = [f"Dilation {se}" for se in seq] + [f"Erosion {se}" for se in seq]

                # Call the function
                verify_solution(tasks, list_ops)
    else:
        task_index = 0  # Example Number
        list_ops = ['Dilation SE2', 'Dilation SE6', 'Dilation SE8', 'Dilation SE6', 'Erosion SE2', 'Erosion SE6',
                    'Erosion SE8', 'Erosion SE6']

        # task_index = 1
        # list_ops = ['Dilation SE7', 'Dilation SE1', 'Dilation SE6', 'Dilation SE8', 'Erosion SE7', 'Erosion SE1',
        #             'Erosion SE6', 'Erosion SE8']
        #
        # task_index = 9
        # list_ops = ['Dilation SE7', 'Dilation SE7', 'Dilation SE1', 'Dilation SE7', 'Erosion SE7', 'Erosion SE7',
        #             'Erosion SE1', 'Erosion SE7']
        #
        # task_index = 16
        # list_ops = ['Dilation SE4', 'Dilation SE5', 'Dilation SE4', 'Dilation SE2', 'Erosion SE4', 'Erosion SE5',
        #             'Erosion SE4', 'Erosion SE2']
        task_index = 84
        list_ops = ['Dilation SE1', 'Dilation SE5', 'Dilation SE7', 'Dilation SE8', 'Erosion SE1', 'Erosion SE5',
                    'Erosion SE7', 'Erosion SE8']
        print(f"Task: {task_index}")

        # Load the dataset
        catA_path = "../Dataset/CatA_Simple/Task{:03d}"
        with open((catA_path + ".json").format(task_index), 'r') as f:
            tasks = json.load(f)
        # Load the solution.
        # with open((catA_path + "_soln.txt").format(task_index), 'r') as f:
        #     list_ops = f.readlines()

        verify_solution(tasks, list_ops)



