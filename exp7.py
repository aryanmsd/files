from itertools import combinations

def knapsack_brute_force(weights, values, capacity):
    n = len(weights)
    max_value = 0
    best_combination = []

    # Generate all subsets of items
    for i in range(1, n + 1):
        for subset in combinations(range(n), i):  # All subsets of size i
            total_weight = sum(weights[j] for j in subset)
            total_value = sum(values[j] for j in subset)

            if total_weight <= capacity and total_value > max_value:
                max_value = total_value
                best_combination = subset

    return max_value, best_combination

# User input
n = int(input("Enter the number of items: "))

weights = []
values = []

print("Enter weight and value for each item:")
for i in range(n):
    w, v = map(int, input(f"Item {i+1} (weight value): ").split())
    weights.append(w)
    values.append(v)

capacity = int(input("Enter knapsack capacity: "))

# Solve Knapsack
max_value, items = knapsack_brute_force(weights, values, capacity)

# Display result
print(f"\nMaximum Value: {max_value}")
print(f"Selected Items: {[i+1 for i in items]} (1-based index)")
