import matplotlib.pyplot as plt

# Data from your specific results
routes = ['Route 1', 'Route 2', 'Route 3']
stops = [1, 3, 20]  # Stops per route
distances = [0.11, 0.26, 2.93]
vehicles_budgeted = 4
vehicles_used = 3

# --- GRAPH 1: Workload Imbalance (Stops per Driver) ---
plt.figure(figsize=(8, 5))
bars = plt.bar(routes, stops, color=['#4CAF50', '#2196F3', '#F44336'])
plt.title('Workload Distribution: Stops per Vehicle', fontsize=14)
plt.xlabel('Vehicle Route', fontsize=12)
plt.ylabel('Number of Customer Stops', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add numbers on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, int(yval), ha='center', fontweight='bold')

plt.savefig('workload_graph.png')
print("Graph 1 saved as workload_graph.png")

# --- GRAPH 2: Resource Savings (Budget vs Actual) ---
plt.figure(figsize=(6, 6))
labels = ['Budgeted Fleet', 'Optimized Fleet']
values = [vehicles_budgeted, vehicles_used]
plt.bar(labels, values, color=['gray', 'green'])
plt.title('Resource Efficiency: Fleet Usage', fontsize=14)
plt.ylabel('Number of Vehicles', fontsize=12)
plt.yticks(range(0, 6))

plt.savefig('efficiency_graph.png')
print("Graph 2 saved as efficiency_graph.png")