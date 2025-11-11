import pandas as pd
import numpy as np

# Read the original CSV file
df = pd.read_csv('catB_hard_solutions_randomised.csv')

# Split into two dataframes based on solution being None or NaN
solved_tasks = df[df['solution'].notna() & (df['solution'] != 'None')]
unsolved_tasks = df[df['solution'].isna() | (df['solution'] == 'None')]

# Save to separate CSV files
solved_tasks.to_csv('catB_randomised_solved_tasks.csv', index=False)
unsolved_tasks.to_csv('catB_randomised_unsolved_tasks.csv', index=False)

print(f"Total tasks: {len(df)}")
print(f"Solved tasks: {len(solved_tasks)}")
print(f"Unsolved tasks: {len(unsolved_tasks)}")