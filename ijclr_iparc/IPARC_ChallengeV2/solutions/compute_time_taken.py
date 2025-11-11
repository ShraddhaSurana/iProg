import pandas as pd

# Load the CSV file
file_path = 'catA_simple_chatgpt_task_results.csv'
df = pd.read_csv(file_path)

# Calculate the average time taken
average_time = df['time_taken'].mean()
# average_time = df['Time_Taken'].mean()

print(f"Average time taken per task: {average_time:.4f} seconds")