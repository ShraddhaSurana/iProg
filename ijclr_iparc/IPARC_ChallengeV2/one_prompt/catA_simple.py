import json
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion
from itertools import product
from time import time

# Load Task000.json
with open("../Dataset/CatA_Simple/Task001.json", "r") as f:
    task_data = json.load(f)

# Extract input-output pairs
pairs = [(np.array(io["input"], dtype=bool), np.array(io["output"], dtype=bool)) for io in task_data]

# Define structuring elements
SEs = {
    "SE1": np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], dtype=bool),
    "SE2": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
    "SE3": np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool),
    "SE4": np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=bool),
    "SE5": np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]], dtype=bool),
    "SE6": np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]], dtype=bool),
    "SE7": np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=bool),
    "SE8": np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]], dtype=bool)
}

# Generate all 4-length combinations of SE keys
se_keys = list(SEs.keys())
candidates = product(se_keys, repeat=4)

# Search for a valid sequence
start_time = time()
solution = None

# Re-run search with corrected assumption:
# Erosion SEs should be applied in the SAME ORDER as dilation SEs (not reversed)

start_time = time()
solution = None

# Reiterate through all possible 4-SE dilation sequences
for candidate in product(se_keys, repeat=4):
    success = True
    for input_img, output_img in pairs:
        temp = input_img.copy()
        # Apply dilations
        for key in candidate:
            temp = binary_dilation(temp, structure=SEs[key])
        # Apply erosions in the SAME ORDER
        for key in candidate:
            temp = binary_erosion(temp, structure=SEs[key])
        if not np.array_equal(temp, output_img):
            success = False
            break
    if success:
        solution = candidate
        break

end_time = time()
elapsed = end_time - start_time

print(solution, elapsed)




