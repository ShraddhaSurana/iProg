import subprocess

processes = []
num_instances = 20

for i in range(num_instances):
    print(f"Launching instance {i + 1}")
    p = subprocess.Popen(["python3", "catA_Hard_with_randomization.py"])
    processes.append(p)

for p in processes:
    p.wait()

print("All instances finished.")