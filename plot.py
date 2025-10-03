import matplotlib.pyplot as plt

# Read results from BackTracking_Result.txt
bt_n = []
bt_time = []
with open("BackTracking_Result.txt", "r") as f:
	lines = [line.strip() for line in f if line.strip()]
	for i in range(0, len(lines), 2):
		bt_n.append(int(lines[i]))
		bt_time.append(float(lines[i+1]))

plt.figure(figsize=(8, 6))

# Plot backtracking algorithm results
plt.plot(bt_n, bt_time, marker='o', label='Backtracking Algorithm')

## Now our algorithm
alg_n = []
alg_time = []

with open("Result.txt", "r") as f:
	lines = [line.strip() for line in f if line.strip()]
	for i in range(0, len(lines), 2):
		alg_n.append(int(lines[i]))
		alg_time.append(float(lines[i+1]))

#plot algorithm result
plt.plot(alg_n, alg_time, marker='o', label='Evolutionary Algorithm')		



# Labels and title
plt.xlabel("Problem Size (n)")
plt.ylabel("Execution Time (s)")
plt.title("Algorithms Runtime")
plt.legend()
plt.grid(True)

plt.show()
